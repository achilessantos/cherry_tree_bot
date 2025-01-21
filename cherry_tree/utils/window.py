import pygetwindow as gw


def restore_window(game_window_name):
    window = gw.getWindowsWithTitle(game_window_name)[0]

    if window.left < 0:
        window.restore()

    return window.activate()


def is_active(game_window_name):
    window = gw.getWindowsWithTitle(game_window_name)[0]

    return window.isActive()
