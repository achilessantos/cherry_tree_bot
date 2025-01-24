from time import time
from abc import ABC, abstractmethod
from cherry_tree.gameplay.typings import Context
from .task_status import TaskStatus


class BaseTask(ABC):
    """
    Representa uma tarefa básica com controle de status, delays e reinicializações.

    Atributos:
        delay_before_start (int): Tempo de atraso antes do início.
        delay_after_complete (int): Tempo de atraso após a conclusão.
        delay_of_timeout (int): Tempo limite para execução da tarefa.
        is_root_task (bool): Indica se é a tarefa raiz.
        manually_terminable (bool): Indica se a tarefa pode ser terminada manualmente.
        name (str): Nome da tarefa.
        parent_task (BaseTask): Referência à tarefa pai.
        should_timeout_tree_when_timeout (bool): Indica se o timeout deve se propagar.
        status (TaskStatus): Status atual da tarefa.
    """

    def __init__(
        self,
        delay_before_start=0,
        delay_after_complete=0,
        delay_of_timeout=0,
        is_root_task=False,
        manually_terminable=False,
        name="baseTask",
        parent_task=None,
        should_timeout_tree_when_timeout=False,
    ):
        if delay_before_start < 0 or delay_after_complete < 0 or delay_of_timeout < 0:
            raise ValueError("Delays devem ser valores não negativos.")

        self.created_at = time()
        self.started_at = None
        self.finished_at = None
        self.terminable = True
        self.delay_before_start = delay_before_start
        self.delay_after_complete = delay_after_complete
        self.delay_of_timeout = delay_of_timeout
        self.is_retrying = False
        self.is_root_task = is_root_task
        self.manually_terminable = manually_terminable
        self.name = name
        self.parent_task = parent_task
        self.retry_count = 0
        self.root_task = None
        self.should_timeout_tree_when_timeout = should_timeout_tree_when_timeout
        self.status = TaskStatus.NOT_STARTED.value
        self.status_reason = None

    def set_parent_task(self, parent_task):
        """
        Define a tarefa pai desta tarefa.
        Args:
            parent_task (BaseTask): A tarefa pai.
        Returns:
            self: Retorna a própria instância para encadeamento.
        """
        self.parent_task = parent_task
        return self

    def set_root_task(self, root_task):
        """
        Define a tarefa raiz desta tarefa.
        Args:
            root_task (BaseTask): A tarefa raiz.
        Returns:
            self: Retorna a própria instância para encadeamento.
        """
        self.root_task = root_task
        return self

    def reset(self):
        """
        Reseta a tarefa para o estado inicial.
        """
        self.started_at = None
        self.finished_at = None
        self.status = TaskStatus.NOT_STARTED.value
        self.status_reason = None
        self.retry_count = 0

    def has_delay_passed(self, start_time: float, delay: float) -> bool:
        """
        Verifica se o delay desde `start_time` passou.
        Args:
            start_time (float): Tempo inicial.
            delay (float): Delay esperado.
        Returns:
            bool: True se o delay passou, False caso contrário.
        """
        return time() - start_time >= delay

    @abstractmethod
    def execute(self, context: Context) -> Context:
        """
        Executa a lógica principal da tarefa.
        Deve ser implementado por subclasses.
        Args:
            context (Context): Contexto de execução.
        Returns:
            Context: Contexto atualizado após execução.
        """
        return context

    def should_ignore(self, _: Context) -> bool:
        """
        Determina se a tarefa deve ser ignorada.
        Args:
            _ (Context): Contexto de execução.
        Returns:
            bool: False por padrão.
        """
        return False

    def did(self, _: Context) -> bool:
        return True

    def ping(self, context: Context) -> Context:
        return context

    def should_manually_complete(self, _: Context) -> bool:
        """
        Determina se a tarefa deve ser manualmente completada.
        Args:
            _ (Context): Contexto de execução.
        Returns:
            bool: False por padrão.
        """
        return False

    def should_restart(self, _: Context) -> bool:
        """
        Determina se a tarefa deve reiniciar.
        Args:
            _ (Context): Contexto de execução.
        Returns:
            bool: False por padrão.
        """
        return False

    def on_before_start(self, context: Context) -> Context:
        """
        Hook chamado antes do início da tarefa.
        Args:
            context (Context): Contexto de execução.
        Returns:
            Context: Contexto atualizado.
        """
        return context

    def on_before_restart(self, context: Context) -> Context:
        """
        Hook chamado antes de reiniciar a tarefa.
        Args:
            context (Context): Contexto de execução.
        Returns:
            Context: Contexto atualizado.
        """
        return context

    def on_ignored(self, context: Context) -> Context:
        """
        Hook chamado quando a tarefa é ignorada.
        Args:
            context (Context): Contexto de execução.
        Returns:
            Context: Contexto atualizado.
        """
        return context

    def on_interrupt(self, context: Context) -> Context:
        """
        Hook chamado quando a tarefa é interrompida.
        Args:
            context (Context): Contexto de execução.
        Returns:
            Context: Contexto atualizado.
        """
        return context

    def on_complete(self, context: Context) -> Context:
        """
        Hook chamado após a conclusão da tarefa.
        Args:
            context (Context): Contexto de execução.
        Returns:
            Context: Contexto atualizado.
        """
        return context

    def on_timeout(self, context: Context) -> Context:
        """
        Hook chamado quando a tarefa atinge o timeout.
        Args:
            context (Context): Contexto de execução.
        Returns:
            Context: Contexto atualizado.
        """
        return context

    def __repr__(self):
        """
        Retorna uma representação legível da tarefa.
        """
        return (
            f"BaseTask(name={self.name}, status={self.status}, "
            f"delay_before_start={self.delay_before_start}, delay_after_complete={self.delay_after_complete})"
        )
