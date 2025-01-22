"""Main application"""

from cherry_tree.gameplay.threads.cherry_tree import CherryTreeThread
from cherry_tree.gameplay.context import CONTEXT
from cherry_tree.ui.context import Context
from cherry_tree.utils.log import setup_custom_logger

logger = setup_custom_logger("main")


def main():
    logger.info("Initializing application...")

    context_instance = Context(CONTEXT)
    cherry_tree_bot_instance = CherryTreeThread(context_instance)
    cherry_tree_bot_instance.mainloop()
    # matchingWindows = gw.getWindowsWithTitle(game_window)[0]
    # print(matchingWindows)
    # print(matchingWindows.isMaximized)
    # print(matchingWindows.isActive)
    # print(matchingWindows.visible)
    # matchingWindows.restore()
    # print(matchingWindows.isActive)

    # return contextIstance
    # print(game_window)
    # matchingWindows = pygetwindow.getWindowsWithTitle(game_window)[0]
    # print(matchingWindows)
    # matchingWindows.activate()
    # matchingWindows.minimize()
    # time.sleep(2)
    # matchingWindows.restore()
    # activate_window()
    # print('hello world')


if __name__ == "__main__":
    main()
