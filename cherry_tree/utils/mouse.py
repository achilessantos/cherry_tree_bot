import pyautogui
from cherry_tree.shared.typings import XYCoordinate


def left_click(window_coordinate: XYCoordinate = None):
    if window_coordinate is None:
        pyautogui.leftClick()
        return
    pyautogui.leftClick(window_coordinate[0], window_coordinate[1])


def right_click(window_coordinate: XYCoordinate = None):
    if window_coordinate is None:
        pyautogui.rightClick()
        return
    pyautogui.rightClick(window_coordinate[0], window_coordinate[1])


def scroll(clicks: int):
    pyautogui.scroll(clicks)
