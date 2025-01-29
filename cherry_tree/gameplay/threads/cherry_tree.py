import sys
import logging
import threading
import traceback
from time import sleep, time
import keyboard
import pyautogui
from cherry_tree.gameplay.core.middleware.screenshot import set_screenshot_middleware
from cherry_tree.gameplay.core.middleware.game_window import (
    set_game_window_middleware,
)
from cherry_tree.gameplay.core.middleware.tasks import set_clean_up_tasks_middleware
from cherry_tree.gameplay.core.tasks.collect_loot import CollectLootTask
from cherry_tree.gameplay.core.tasks.select_menu import SelectMenuTask
from cherry_tree.gameplay.core.tasks.select_menu_option import SelectMenuOptionTask
from cherry_tree.gameplay.core.tasks.set_combat_mode import SetCombatModeTask
from cherry_tree.gameplay.core.tasks.slayer import SlayerTask
from cherry_tree.gameplay.typings import Context


logger = logging.getLogger("main")
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

DEFAULT_COMBAT_MODE = "strength"
HOTKEYS = {"quit_game": "ctrl+alt+q", "pause_continue": "ctrl+alt+p"}


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
            context (Any): The shared context for the game data./
        """
        self.context = context
        # self.should_exit = threading.Event()
        self._start_keyboard_listener()

    def mainloop(self):
        """
        Run the main loop of the thread, processing game data.
        """
        logger.info("Starting mainloop of CherryTreeThread")
        while True:
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
        print("orchestrator.tasks_queue OUT", orchestrator.tasks_queue)
        print("orchestrator.current_task OUT", orchestrator.current_task)

        # Adicionar novas tarefas à fila (exemplo de múltiplas tarefas)
        if not orchestrator.tasks_queue and not orchestrator.current_task:
            orchestrator.add_task(CollectLootTask())
            # orchestrator.add_task(SetCombatModeTask())
            # orchestrator.add_task(SelectMenuTask())
            # orchestrator.add_task(SelectMenuOptionTask())
            orchestrator.add_task(SlayerTask())

            print("orchestrator.tasks_queue INNER", orchestrator.tasks_queue)
            print("orchestrator.current_task INNER", orchestrator.current_task)

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

    def _start_keyboard_listener(self):
        """Inicia um listener para detectar as hotkeys"""

        for action, key_combination in HOTKEYS.items():
            # Cria uma função dinâmica para cada ação
            def create_action_callback(action_name):
                def callback():
                    logger.info(
                        "Tecla {key_combination} pressionada! Executando ação: %s",
                        action_name
                    )
                    self._execute_action(action_name)

                return callback

            # Registra a hotkey com a função de callback correspondente
            keyboard.add_hotkey(key_combination, create_action_callback(action))

        # Inicia o listener em uma thread separada
        keyboard_thread = threading.Thread(target=keyboard.wait)
        keyboard_thread.daemon = (True) # Define a thread como daemon para encerrar com o programa
        keyboard_thread.start()
        logger.info("Listener de teclas iniciado. Hotkeys registradas: %s", HOTKEYS)

    def _execute_action(self, action_name):
        """
        Executa a ação correspondente ao nome da ação.
        :param action_name: Nome da ação a ser executada.
        """
        match action_name:
            case "quit_game":
                self._custom_action_quit_game()
            case "pause_continue":
                self._custom_action_pause_continue()
            case _:
                logger.warning("Ação '%s' não reconhecida.", action_name)

    def _custom_action_quit_game(self):
        """Ação personalizada para encerrar o jogo."""
        logger.info("Executando ação personalizada: Encerrar o jogo.")
        # Adicione aqui a lógica para encerrar o jogo
        # set = self.should_exit.set()
        # print("set", set)
        # sys.exit(0)

    def _custom_action_pause_continue(self):
        """Ação personalizada a ser executada quando CTRL+ALT+P for pressionado."""

        if self.context.context["pause"]:
            logger.info("Continunando a execução do bot.")
            self.context.context["pause"] = False
        else:
            logger.info("Pausando a execução do bot.")
            self.context.context["pause"] = True
