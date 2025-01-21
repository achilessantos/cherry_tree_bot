import cv2
import dxcam
from typing import Union
from cherry_tree.shared.typings import BBox


camera = dxcam.create(output_color="BGRA")
latest_screenshot = None


def get_screenshot():
    global camera, latest_screenshot

    screenshot = camera.grab()
    if screenshot is None:
        return latest_screenshot

    latest_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)

    return latest_screenshot


def locate(screenshot, template, confidence: float = 0.85) -> Union[BBox, None]:
    match = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, confidence_result, _, max_locate = cv2.minMaxLoc(match)
    template_width, template_height = template.shape[::-1]
    width_to_click = max_locate[0] + template_width // 2
    height_to_click = max_locate[1] + template_height // 2

    if confidence_result <= confidence:
        raise Exception("Error - Confidence matching was below {confidence}.")

    return width_to_click, height_to_click, template_width, template_height


def prepare_image(image_path):
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
