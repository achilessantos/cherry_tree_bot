from cherry_tree.gameplay.typings import Context
from cherry_tree.gameplay.core.tasks.orchestrator.task_status import TaskStatus


def set_clean_up_tasks_middleware(context: Context) -> Context:
    """
    Middleware para limpar tarefas quando necessário.
    """
    orchestrator = context["tasksOrchestrator"]

    # Obter a tarefa atual diretamente do Orchestrator
    current_task = orchestrator.current_task

    # Se não houver tarefa atual, ou se estiver concluída, limpar a fila
    if current_task and current_task.status == TaskStatus.COMPLETED.value:
        orchestrator.reset()
    elif (
        orchestrator.root_task
        and orchestrator.root_task.status == TaskStatus.COMPLETED.value
    ):
        orchestrator.reset()

    return context
