from config import images
import pyautogui as pg
from cherry_tree.utils.image import find_image


def get_combat_mode(game_window_name, combat_mode="strength_mode"):
    image_path = images["combatMode"].get(combat_mode)
    print(image_path)
    print(game_window_name)
    # print(find_image(image_path, game_window_name))
    # locate = pg.locateOnWindow("./images/combat_mode/{combat_mode}.png", title=game_window_name)
    locate = pg.locateOnWindow("./images/combat_mode/strength_mode.png", title=game_window_name)
    print(locate)
    return image_path


get_combat_mode("CherryTree - Text RPG", "strength_mode")
