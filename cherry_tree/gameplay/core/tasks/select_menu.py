import logging

from cherry_tree.gameplay.core.tasks.orchestrator.base import BaseTask
from cherry_tree.gameplay.core.tasks.orchestrator.task_status import TaskStatus
from cherry_tree.gameplay.typings import Context
from cherry_tree.repositories.game_window.core import get_menu
from cherry_tree.utils.mouse import left_click


logger = logging.getLogger("main")


class SelectMenuTask(BaseTask):
    def __init__(self):
        super().__init__(
            name="select_menu",
            delay_before_start=0.5,
            delay_after_complete=0.5,
        )

    def execute(self, context: Context) -> Context:
        coordinate = get_menu(context["screenshot"])

        if coordinate:
            left_click(coordinate)
            logger.info("Menu was selected.")
            self.status = TaskStatus.COMPLETED.value

        return context
