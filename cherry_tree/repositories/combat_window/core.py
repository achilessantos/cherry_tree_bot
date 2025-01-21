import time
import pyautogui as pg
from .config import images
from cherry_tree.utils.core import read_image, locate
from cherry_tree.shared.typings import BBox
from cherry_tree.utils.mouse import left_click


def get_combat_mode(screenshot, combat_mode="strength_mode"):
    image_path = images["combatMode"].get(combat_mode)
    template = read_image(image_path)
    result = locate(screenshot, template)

    if result:
        set_combat_mode(result)
        return True

    return False


def set_combat_mode(coordinates: BBox):
    current_mouse_position = pg.position()

    left_click(coordinates)
    time.sleep(0.12)
    pg.moveTo(current_mouse_position)
