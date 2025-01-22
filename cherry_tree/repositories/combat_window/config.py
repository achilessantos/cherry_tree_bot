from pathlib import Path


ABSOLUTE_PATH = Path(__file__).parent.resolve()
ROOT_DIR = Path.cwd()
RELATIVE_PATH = ABSOLUTE_PATH.relative_to(ROOT_DIR)
IMAGES_PATH = f"{RELATIVE_PATH}\\images"
COMBAT_MODE_PATH = f"{IMAGES_PATH}\\combat_mode"
BUTTONS_PATH = f"{IMAGES_PATH}\\buttons"
MESSAGES_PATH = f"{IMAGES_PATH}\\messages"
IMAGES = {
    "combatMode": {
        "attack_mode": f"{COMBAT_MODE_PATH}\\attack_mode.png",
        "defense_mode": f"{COMBAT_MODE_PATH}\\defense_mode.png",
        "strength_mode": f"{COMBAT_MODE_PATH}\\strength_mode.png",
        "unchecked_attack_mode": f"{COMBAT_MODE_PATH}\\unchecked_attack_mode.png",
        "unchecked_defense_mode": f"{COMBAT_MODE_PATH}\\unchecked_defense_mode.png",
        "unchecked_distance_mode": f"{COMBAT_MODE_PATH}\\unchecked_distance_mode.png",
        "unchecked_strength_mode": f"{COMBAT_MODE_PATH}\\unchecked_strength_mode.png",
    },
    "buttons": {
        "collectLoots": f"{BUTTONS_PATH}\\collectLoots.png",
        "leave": f"{BUTTONS_PATH}\\leave.png",
        "menu": f"{BUTTONS_PATH}\\menu.png",
        "potionMenu": f"{BUTTONS_PATH}\\potionMenu.png",
    },
    "messages": {
        "searchingForEnemy": f"{MESSAGES_PATH}\\searchingForEnemy.png",
        "slayerKillsLeft": f"{MESSAGES_PATH}\\slayerKillsLeft.png",
    },
}
