import time
import pyautogui as pg
from cherry_tree.utils.core import read_image, locate
from cherry_tree.shared.typings import BBox
from cherry_tree.utils.mouse import left_click
from cherry_tree.repositories.combat_window.config import IMAGES


def get_combat_mode(screenshot, combat_mode="strength_mode"):
    image_path = IMAGES["combatMode"].get(combat_mode)
    template = read_image(image_path)
    result = locate(screenshot, template)

    if result:
        return result

    return None


def get_collect_loot_coordinate(screenshot):
    try:
        image_path = IMAGES["buttons"].get("collectLoots")
        template = read_image(image_path)
        result = locate(screenshot, template)

        if result:
            return result
        
        raise ValueError("Falha na coleta do loot.")
    except ValueError as e:
        return None


def set_combat_mode(coordinates: BBox):
    current_mouse_position = pg.position()

    left_click(coordinates)
    time.sleep(0.12)
    pg.moveTo(current_mouse_position)
