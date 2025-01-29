from pathlib import Path


ABSOLUTE_PATH = Path(__file__).parent.resolve()
ROOT_DIR = Path.cwd()
RELATIVE_PATH = ABSOLUTE_PATH.relative_to(ROOT_DIR)
IMAGES_PATH = f"{RELATIVE_PATH}\\images"
BUTTONS_PATH = f"{IMAGES_PATH}\\buttons"
IMAGES = {
    "buttons": {
        "menu": f"{BUTTONS_PATH}\\menu.png",
        "potionMenu": f"{BUTTONS_PATH}\\potionMenu.png",
    }
}
