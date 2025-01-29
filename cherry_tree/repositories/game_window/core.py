from cherry_tree.utils.window import restore_window
from cherry_tree.utils.core import read_image, locate
from cherry_tree.repositories.game_window.config import IMAGES


def is_activated_game_window(game_window_name):
    restore_window(game_window_name)

    return True


def get_menu(screenshot):
    image_path = IMAGES["buttons"].get("menu")
    template = read_image(image_path)
    result = locate(screenshot, template)

    if result:
        return result

    return None
