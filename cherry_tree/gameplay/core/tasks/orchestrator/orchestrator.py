from time import sleep, time
from typing import Optional
from collections import deque
from ....typings import Context
from .base import BaseTask
from .task_status import TaskStatus



class TasksOrchestrator:
    def __init__(self):
        self.tasks_queue = deque()  # Fila de tarefas
        self.root_task: Optional[BaseTask] = None
        self.current_task: Optional[BaseTask] = None

    def set_root_task(self, context: Context, task: BaseTask):
        """Sets the root task and interrupts the current task if needed."""
        current_task = self.get_current_task(context)

        if current_task:
            self.interrupt_tasks(context, current_task)
        if task:
            task.is_root_task = True
        self.root_task = task

    def interrupt_tasks(self, context: Context, task: BaseTask) -> Context:
        """Interrupts the task and its parent tasks."""
        context = task.on_interrupt(context)
        if task.parent_task:
            return self.interrupt_tasks(context, task.parent_task)
        return context

    def reset(self):
        """Reseta a fila e o estado do orquestrador."""
        self.tasks_queue.clear()
        self.current_task = None

    def get_current_task(self, context: Context) -> Optional[BaseTask]:
        """Retrieves the currently active task."""
        return self._get_nested_task(self.root_task, context)

    def get_current_task_name(self, context: Context) -> str:
        """Gets the name of the current task."""
        current_task = self.get_current_task(context)
        if not current_task:
            return "unknown"
        return (
            current_task.name
            if current_task.is_root_task
            else current_task.root_task.name
        )
    
    def add_task(self, task: BaseTask):
        """Adiciona uma nova tarefa à fila."""
        self.tasks_queue.append(task)

    def set_next_task(self):
        """Define a próxima tarefa da fila como a atual."""
        if self.tasks_queue:
            self.current_task = self.tasks_queue.popleft()
            self.current_task.reset()


    def execute(self, context: Context) -> Context:
        """Executa todas as tarefas da fila na mesma iteração."""
        while self.tasks_queue or self.current_task:
            if not self.current_task:
                self.set_next_task()

            if not self.current_task:
                break  # Não há mais tarefas para executar

            # Delay antes de iniciar a tarefa
            if self.current_task.status == TaskStatus.NOT_STARTED.value:
                if self.current_task.delay_before_start:
                    sleep(self.current_task.delay_before_start)
                self.current_task.status = TaskStatus.RUNNING.value

            # Executa a tarefa
            if self.current_task.status == TaskStatus.RUNNING.value:
                context = self.current_task.execute(context)            

            # Delay após completar a tarefa
            if self.current_task.status == TaskStatus.COMPLETED.value:
                context = self.current_task.on_complete(context)
                if self.current_task.delay_after_complete:
                    sleep(self.current_task.delay_after_complete)
                self.current_task = None  # Finaliza a tarefa atual            

        return context


    def _get_nested_task(self, task: Optional[BaseTask], context: Context) -> Optional[BaseTask]:
        """
        Recupera a tarefa aninhada com base no contexto, priorizando o current_task.
        """
        if self.current_task:  # Verifica se há uma tarefa atual definida
            return self.current_task

        # Caso contrário, utiliza a lógica baseada na root_task
        if not task:
            return None

        if hasattr(task, "tasks"):
            if task.status == TaskStatus.NOT_STARTED.value:
                context = task.on_before_start(context)
                task.status = TaskStatus.RUNNING.value
            if task.status != TaskStatus.COMPLETED.value:
                if not task.tasks:
                    return task
                return self._get_nested_task(
                    task.tasks[task.current_task_index], context
                )
        return task

    def _check_hooks(self, current_task: BaseTask, context: Context) -> Context:
        """Checks and applies hooks for restarting or completing tasks."""
        if current_task.manually_terminable and current_task.should_manually_complete(
            context
        ):
            return self._mark_task_as_finished(
                current_task, context, disable_manual_termination=True
            )

        if (
            current_task.status != TaskStatus.NOT_STARTED.value
            and current_task.should_restart(context)
        ):
            current_task.status = TaskStatus.NOT_STARTED.value
            current_task.retry_count += 1
            if hasattr(current_task, "tasks"):
                current_task.current_task_index = 0
            context = current_task.on_before_restart(context)

        if current_task.parent_task:
            self._check_hooks(current_task.parent_task, context)
        return context

    def _handle_tasks(self, context: Context) -> Context:
        """Handles the execution flow of tasks."""
        if not self.root_task or self.root_task.status == TaskStatus.COMPLETED.value:
            return context

        current_task = self.get_current_task(context)
        if not current_task:
            return context

        if current_task.status == TaskStatus.AWAITING_MANUAL_TERMINATION.value:
            if current_task.should_manually_complete(context):
                return self._mark_task_as_finished(
                    current_task, context, disable_manual_termination=True
                )
            if current_task.should_restart(context) and not current_task.is_restarting:
                current_task.started_at = None
                current_task.status = TaskStatus.NOT_STARTED.value
                current_task.is_restarting = True
                current_task.retry_count += 1
                return current_task.on_before_restart(context)

        if current_task.status in (
            TaskStatus.NOT_STARTED.value,
            TaskStatus.AWAITING_DELAY_BEFORE_START.value,
        ):
            current_task.is_restarting = False
            if current_task.started_at is None:
                current_task.started_at = time()
            context = current_task.on_before_start(context)
            if self._has_elapsed_time(current_task, current_task.delay_before_start):
                if current_task.should_ignore(context):
                    context = current_task.on_ignored(context)
                    return self._mark_task_as_finished(current_task, context)
                current_task.status = TaskStatus.RUNNING.value
                return current_task.execute(context)
            current_task.status = TaskStatus.AWAITING_DELAY_BEFORE_START.value

        elif current_task.status == TaskStatus.RUNNING.value:
            if not current_task.terminable:
                context = current_task.ping(context)
                return current_task.execute(context)
            if current_task.should_restart(context):
                current_task.status = TaskStatus.NOT_STARTED.value
                return context
            if self._has_timed_out(current_task):
                context = current_task.on_timeout(context)
                return self._mark_task_as_finished(current_task, context, timeout=True)
            if current_task.did(context):
                current_task.finished_at = time()
                if current_task.delay_after_complete > 0:
                    current_task.status = TaskStatus.AWAITING_DELAY_TO_COMPLETE.value
                    return context
                return self._mark_task_as_finished(current_task, context)
            context = current_task.ping(context)

        elif current_task.status == TaskStatus.AWAITING_DELAY_TO_COMPLETE.value:
            if self._has_elapsed_time(current_task, current_task.delay_after_complete):
                return self._mark_task_as_finished(current_task, context)

        return context

    def _mark_task_as_finished(
        self,
        task: BaseTask,
        context: Context,
        disable_manual_termination=False,
        timeout=False,
    ) -> Context:
        """Marks a task as finished and handles parent tasks if needed."""
        if task.manually_terminable and not disable_manual_termination:
            task.status = TaskStatus.AWAITING_MANUAL_TERMINATION.value
            return context

        task.status = TaskStatus.COMPLETED.value
        task.status_reason = (
            TaskStatus.TIMEOUT.value if timeout else TaskStatus.COMPLETED.value
        )
        context = task.on_complete(context)

        if task.parent_task:
            if timeout:
                context = task.parent_task.on_timeout(context)
                return self._mark_task_as_finished(
                    task.parent_task, context, timeout=True
                )

            if task.parent_task.current_task_index < len(task.parent_task.tasks) - 1:
                task.parent_task.current_task_index += 1
            else:
                if task.parent_task.should_restart_after_all_childrens_complete(
                    context
                ):
                    task.parent_task.status = TaskStatus.NOT_STARTED.value
                    task.parent_task.current_task_index = 0
                    task.parent_task.retry_count += 1
                    return task.parent_task.on_before_restart(context)
                return self._mark_task_as_finished(task.parent_task, context)

        return context

    def _has_elapsed_time(self, task: BaseTask, delay: float) -> bool:
        """Checks if the required delay time has elapsed."""
        return time() - (task.started_at or 0) >= delay

    def _has_timed_out(self, task: BaseTask) -> bool:
        """Checks if the task has timed out."""
        return (
            task.delay_of_timeout > 0
            and time() - (task.started_at or 0) >= task.delay_of_timeout
        )
