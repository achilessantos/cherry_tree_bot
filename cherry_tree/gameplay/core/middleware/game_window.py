from cherry_tree.repositories.game_window.core import active_game_window

# from ...typings import Context


def set_game_window_middleware(context):
    active_game_window(context)
