import logging
from cherry_tree.gameplay.core.tasks.orchestrator.base import BaseTask
from cherry_tree.gameplay.core.tasks.orchestrator.task_status import TaskStatus
from cherry_tree.gameplay.typings import Context
from cherry_tree.repositories.combat_window.core import get_collect_loot_coordinate
from cherry_tree.utils.mouse import left_click


logger = logging.getLogger("main")


class CollectLootTask(BaseTask):
    def __init__(self):
        super().__init__(
            name="collect_loot",
            delay_before_start=0.5,
            delay_after_complete=0.5,
        )

    def execute(self, context: Context) -> Context:
        coordinate = get_collect_loot_coordinate(context["screenshot"])

        if coordinate:
            left_click(coordinate)
            logger.info("Loot was collected!")
            self.status = TaskStatus.COMPLETED.value
        else:
            logger.info("Failed to collect loot!")
            self.status = TaskStatus.ERROR.value

        return context
