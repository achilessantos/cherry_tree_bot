from pathlib import Path

ABSOLUTE_PATH = Path(__file__).parent.resolve()
ROOT_DIR = Path.cwd()
RELATIVE_PATH = ABSOLUTE_PATH.relative_to(ROOT_DIR)
IMAGES_PATH = f"{RELATIVE_PATH}\\images"
BUTTONS_PATH = f"{IMAGES_PATH}\\buttons"
IMAGES = {
    "buttons": {
        "slayer_button": f"{BUTTONS_PATH}\\slayer_button.png",
        "select_new_task": f"{BUTTONS_PATH}\\select_new_task.png",
        "select_water_dragon": f"{BUTTONS_PATH}\\select_water_dragon.png",
        "select_slayer_master": f"{BUTTONS_PATH}\\select_slayer_master.png",
        "check_slayer_kills_left": f"{BUTTONS_PATH}\\check_slayer_kills_left.png",
        "click_down_current_slayer_task": f"{BUTTONS_PATH}\\click_down_current_slayer_task.png",
        "slayer_screen": f"{BUTTONS_PATH}\\slayer_screen.png",
        "no_active_task": f"{BUTTONS_PATH}\\no_active_task.png",
    }
}
