"""Tests from mouse helper"""

from cherry_tree.utils.mouse import left_click, right_click, scroll


def test_should_call_left_click_without_params_when_window_coordinate_is_none(mocker):
    """Function call left click without params"""
    left_click_spy = mocker.patch("pyautogui.leftClick")
    left_click()
    left_click_spy.assert_called()


def test_should_call_left_click_with_params_when_window_coordinate_is_not_none(mocker):
    """ "Function call left click with params"""
    window_coordinate = (0, 0)
    left_click_spy = mocker.patch("pyautogui.leftClick")
    left_click(window_coordinate)
    left_click_spy.assert_called_once_with(window_coordinate[0], window_coordinate[1])


def test_should_call_scroll_with_correct_params(mocker):
    """Function call scroll"""
    scrolls = 5
    scroll_spy = mocker.patch("pyautogui.scroll")
    scroll(scrolls)
    scroll_spy.assert_called_once_with(scrolls)


def test_should_call_right_click_without_params_when_window_coordinate_is_none(mocker):
    """Function call right click without params"""
    right_click_spy = mocker.patch("pyautogui.rightClick")
    right_click()
    right_click_spy.assert_called()


def test_should_call_right_click_with_params_when_window_coordinate_is_not_none(mocker):
    """Function call right click with params"""
    window_coordinate = (0, 0)
    right_click_spy = mocker.patch("pyautogui.rightClick")
    right_click(window_coordinate)
    right_click_spy.assert_called_once_with(window_coordinate[0], window_coordinate[1])
