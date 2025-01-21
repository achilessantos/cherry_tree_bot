import logging
from time import sleep, time
from cherry_tree.gameplay.core.middleware.screenshot import set_screenshot_middleware
from cherry_tree.gameplay.core.middleware.game_window import (
    set_game_window_middleware,
)
from cherry_tree.gameplay.core.middleware.combat_mode import set_combat_mode_middleware


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
)

DEFAULT_COMBAT_MODE = "strength_mode"

class CherryTreeThread:
    def __init__(self, context):
        self.context = context

    def mainloop(self):
        logging.info("Starting mainloop of CherryTreeThread")
        print(self.context.context)
        start_time = time()
        # print(start_time)
        self.context.context = self.handle_game_data(self.context.context)
        # while True:
        #     try:
        #         if self.context.context['pause']:
        #             continue
        #         startTime = time()
        #         print(startTime)
        #         self.context.context = self.handleGameData(self.context.context)
        #         endTime = time()
        #         diff = endTime - startTime
        #         sleep(max(0.045 - diff, 0))
        #     except:
        #         print('An exception occurred: ', traceback.format_exc())

    def handle_game_data(self, context):
        if context["pause"]:
            return context

        context = set_game_window_middleware(context)
        context = set_screenshot_middleware(context)
        context = set_combat_mode_middleware(context, DEFAULT_COMBAT_MODE)

        return context
