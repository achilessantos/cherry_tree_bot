import logging
from time import sleep
from cherry_tree.gameplay.core.tasks.orchestrator.base import BaseTask
from cherry_tree.gameplay.core.tasks.orchestrator.task_status import TaskStatus
from cherry_tree.gameplay.typings import Context
from cherry_tree.repositories.slayer_masters_window.core import (
    select_slayer_option_on_navigation,
)
from cherry_tree.utils.core import get_screenshot
from cherry_tree.utils.mouse import left_click, scroll


logger = logging.getLogger("main")


class SelectMenuOptionTask(BaseTask):
    def __init__(self):
        super().__init__(
            name="select_menu_option",
            delay_before_start=0.5,
            delay_after_complete=0.5,
        )

    def execute(self, context: Context) -> Context:
        sleep(0.5)
        scroll(-1500)
        print("scrolling down")
        sleep(2)
        # tem que tirar um print da tela e clicar no slayer
        screenshot_of_menu = get_screenshot()
        coordinate = select_slayer_option_on_navigation(screenshot_of_menu)

        if coordinate:
            left_click(coordinate)
            logger.info("Slayer menu was selected.")
            self.status = TaskStatus.COMPLETED.value

        return context
