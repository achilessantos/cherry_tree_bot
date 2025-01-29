from cherry_tree.utils.core import read_image, locate
from cherry_tree.repositories.slayer_masters_window.config import IMAGES


def select_slayer_option_on_navigation(screenshot):
    return get_coordinate(screenshot, "buttons", "slayer_button")


def select_slayer_master(screenshot):
    return get_coordinate(screenshot, "buttons", "select_slayer_master")


def select_new_task(screenshot):
    return get_coordinate(screenshot, "buttons", "select_new_task")


def select_water_dragon(screenshot):
    return get_coordinate(screenshot, "buttons", "select_water_dragon")


def click_down_current_slayer_task(screenshot):
    return get_coordinate(screenshot, "buttons", "click_down_current_slayer_task")


def check_slayer_kills_left(screenshot):
    return get_coordinate(screenshot, "buttons", "check_slayer_kills_left")


def check_if_slayer_window(screenshot):
    return get_coordinate(screenshot, "buttons", "slayer_screen")


def no_active_task(screenshot):
    return get_coordinate(screenshot, "buttons", "no_active_task")


def get_coordinate(screenshot, key, value):
    image_path = IMAGES[key].get(value)
    template = read_image(image_path)
    result = locate(screenshot, template)

    if result:
        return result

    return None
