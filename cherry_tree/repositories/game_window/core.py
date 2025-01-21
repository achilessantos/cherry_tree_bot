from cherry_tree.utils.window import restore_window


def is_activated_game_window(game_window_name):
    restore_window(game_window_name)

    return True
