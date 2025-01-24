import inspect
from cherry_tree.gameplay.typings import Context
from cherry_tree.gameplay.core.tasks.orchestrator.task_status import TaskStatus


def set_clean_up_tasks_middleware(context: Context) -> Context:
    current_task = context["tasksOrchestrator"].get_current_task(context)
    # print("current_task, set_clean_up_tasks_middleware", current_task)
    # print(inspect.getmembers(current_task, lambda a:not(inspect.isroutine(a))))

    if current_task:
        if (
            current_task.is_root_task
            and current_task.status == TaskStatus.COMPLETED.value
        ):
            context["tasksOrchestrator"].reset()

        if (
            current_task.root_task
            and current_task.root_task.status == TaskStatus.COMPLETED.value
        ):
            context["tasksOrchestrator"].reset()

    return context
