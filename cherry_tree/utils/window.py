import pygetwindow as gw


def activate_window(game_window_name):
    window = gw.getWindowsWithTitle(game_window_name)[0]

    return window.activate()


def restore_window(game_window_name):
    window = gw.getWindowsWithTitle(game_window_name)[0]

    return window.restore()


def is_active(game_window_name):
    window = gw.getWindowsWithTitle(game_window_name)[0]

    return window.isActive()
