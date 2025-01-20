import pyautogui as pg


def find_image(image_path, game_window_name):
    pg.locateOnWindow(image_path, title=game_window_name)
