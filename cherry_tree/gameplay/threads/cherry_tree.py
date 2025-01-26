import logging
import traceback
from time import sleep, time
import pyautogui
from cherry_tree.gameplay.core.middleware.screenshot import set_screenshot_middleware
from cherry_tree.gameplay.core.middleware.game_window import (
    set_game_window_middleware,
)
from cherry_tree.gameplay.core.middleware.tasks import set_clean_up_tasks_middleware
from cherry_tree.gameplay.core.tasks.collect_loot import CollectLootTask
from cherry_tree.gameplay.core.tasks.set_combat_mode import SetCombatModeTask
from cherry_tree.gameplay.typings import Context


logger = logging.getLogger("main")
DEFAULT_COMBAT_MODE = "strength"
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class CherryTreeThread:
    """
    Main thread for the CherryTree game logic.

    Attributes:
        context (Any): The shared context for the game data.
    """

    def __init__(self, context: Context):
        """
        Initialize the CherryTreeThread with a given context.

        Args:
            context (Any): The shared context for the game data.
        """
        self.context = context

    def mainloop(self):
        """
        Run the main loop of the thread, processing game data.
        """
        logger.info("Starting mainloop of CherryTreeThread")
        while True:
            sleep(1)
            try:
                if self.context.context["pause"]:
                    continue

                start_time = time()
                self.context.context = self.handle_game_data(self.context.context)
                self.context.context = self.handle_gameplay_tasks(self.context.context)
                self.execute_tasks()
                self.enforce_loop_timing(start_time)

            except Exception:
                self.log_exception()

    def handle_game_data(self, context: Context) -> Context:
        # print(context)
        if context["pause"]:
            return context

        context = set_game_window_middleware(context)
        # sleep(0.2)
        context = set_screenshot_middleware(context)
        # sleep(0.2)
        context = set_clean_up_tasks_middleware(context)
        # sleep(0.2)

        return context

    def handle_gameplay_tasks(self, context: Context) -> Context:
        orchestrator = context["tasksOrchestrator"]

        # Adicionar novas tarefas à fila (exemplo de múltiplas tarefas)
        if not orchestrator.tasks_queue and not orchestrator.current_task:
            orchestrator.add_task(CollectLootTask())
            orchestrator.add_task(SetCombatModeTask())

        return context

    def execute_tasks(self):
        self.context.context = self.context.context["tasksOrchestrator"].execute(
            self.context.context
        )

    def enforce_loop_timing(self, start_time: float):
        end_time = time()
        elapsed = end_time - start_time
        sleep(max(0.045 - elapsed, 0))

    def log_exception(self):
        logger.warning("An exception occurred")

        logger("An exception occurred:", traceback.format_exc())
