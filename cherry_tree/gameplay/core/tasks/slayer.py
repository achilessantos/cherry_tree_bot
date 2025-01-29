import logging
from time import sleep
from cherry_tree.gameplay.core.tasks.orchestrator.base import BaseTask
from cherry_tree.gameplay.core.tasks.orchestrator.task_status import TaskStatus
from cherry_tree.gameplay.typings import Context
from cherry_tree.repositories.game_window.core import get_menu
from cherry_tree.repositories.slayer_masters_window.core import (
    select_slayer_option_on_navigation,
    select_slayer_master,
    select_new_task,
    select_water_dragon,
    click_down_current_slayer_task,
    check_slayer_kills_left,
    check_if_slayer_window,
    no_active_task,
)
from cherry_tree.utils.core import get_screenshot
from cherry_tree.utils.mouse import left_click, scroll

logger = logging.getLogger("main")


class SlayerTask(BaseTask):
    def __init__(self):
        super().__init__(
            name="slayer",
            is_root_task=True,
            delay_before_start=0.5,
            delay_after_complete=0.5,
        )
        self.SLEEP_DELAY = 0.5
        self.SCROLL_AMOUNT = -1500

    def execute(self, context: Context) -> Context:
        try:
            some_window = get_screenshot()
            print("executing")

            if check_if_slayer_window(some_window):
                self._handle_slayer_window(some_window)
            else:
                print("else")
                self._handle_navigation_menu(some_window)
                slayer_option_navigation_coordinate = (
                    self._handle_navigation_menu_slayer_option()
                )

                if self._handle_click_on_navigation_slayer_option(
                    slayer_option_navigation_coordinate
                ):
                    slayer_window = get_screenshot()
                    self._handle_slayer_window(slayer_window)

            return context
        except ValueError as e:
            logger.warning(e)
            self.status = self.status = TaskStatus.ERROR.value
            return None


    def _handle_navigation_menu(self, window):
        print("_handle_navigation_menu")
        menu_screenshot = get_menu(window)

        if not menu_screenshot:
            raise ValueError("Menu was not found!")

        self._click_and_log(menu_screenshot, "Menu was selected.")
        sleep(self.SLEEP_DELAY)
        scroll(self.SCROLL_AMOUNT)
        logger.info("Scrolling down")

    def _handle_navigation_menu_slayer_option(self):
        sleep(self.SLEEP_DELAY)
        slayer_option_navigation = get_screenshot()
        slayer_option_navigation_coordinate = select_slayer_option_on_navigation(
            slayer_option_navigation
        )

        return slayer_option_navigation_coordinate

    def _handle_click_on_navigation_slayer_option(self, coordinate):
        self._click_and_log(coordinate, "Slayer menu was selected.")
        sleep(self.SLEEP_DELAY)

    def _handle_slayer_window(self, slayer_window):
        sleep(self.SLEEP_DELAY)

        if no_active_task(slayer_window):
            logger.info("Task is not activated!")
            self._handle_new_task(slayer_window)
        else:
            self._handle_existing_task(slayer_window)

    def _handle_new_task(self, slayer_window):
        logger.info("Handling new task...")

        slayer_window_coordinate = select_slayer_master(slayer_window)

        if slayer_window_coordinate:
            sleep(self.SLEEP_DELAY)
            select_new_task_coordinate = select_new_task(slayer_window)

            if select_new_task_coordinate:
                self._click_and_log(select_new_task_coordinate, "New task selected.")
                sleep(self.SLEEP_DELAY)

                select_new_task_window = get_screenshot()
                select_water_dragon_coordinate = select_water_dragon(
                    select_new_task_window
                )

                if select_water_dragon_coordinate:
                    self._click_and_log(
                        select_water_dragon_coordinate, "Water dragon selected."
                    )
                    sleep(self.SLEEP_DELAY)

                    slayer_window = get_screenshot()
                    self._join_on_selected_task(slayer_window)

    def _handle_existing_task(self, slayer_window):
        self._join_on_selected_task(slayer_window)

    def _join_on_selected_task(self, slayer_window):
        select_current_task_coordinate = click_down_current_slayer_task(slayer_window)

        if select_current_task_coordinate:
            sleep(self.SLEEP_DELAY)
            logger.info("Current task coordinate: %s", select_current_task_coordinate)
            (x, y, z, a) = select_current_task_coordinate
            coord_to_click = (x + 20, y + 50, z, a)
            left_click(coord_to_click)
            sleep(self.SLEEP_DELAY)

            logger.info("Arrived combat window again!!!!")
            sleep(2)  # Delay necessário para esperar o popup da task selecionada sumir
            self._check_kills()

    def _check_kills(self):
        while True:
            sleep(2)
            combat_window = get_screenshot()
            kills_left = check_slayer_kills_left(combat_window)
            logger.info("Slayer kills is active!")

            if not kills_left:
                logger.info("Slayer task acabou")
                self.status = TaskStatus.COMPLETED.value
                sleep(self.SLEEP_DELAY)
                break

    def _click_and_log(self, coordinates, message):
        left_click(coordinates)
        logger.info(message)
