import os
import logging
from typing import Union
import cv2
import dxcam
from numpy import ndarray
from cherry_tree.shared.typings import BBox


logger = logging.getLogger("main")
camera = dxcam.create(output_color="BGRA")
LATEST_SCREENSHOT = None


def get_screenshot() -> Union[ndarray, None]:
    global camera, LATEST_SCREENSHOT

    logger.info("Capturing screenshot...")
    screenshot = camera.grab()

    if screenshot is None:
        return LATEST_SCREENSHOT

    LATEST_SCREENSHOT = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)

    return LATEST_SCREENSHOT


def locate(
    screenshot: any, template: any, confidence: float = 0.85
) -> Union[BBox, None]:
    if screenshot is None:
        raise ValueError("Screenshot is None. Please provide a valid image.")
    if template is None:
        raise ValueError("Template is None. Please provide a valid template image.")

    method = cv2.TM_CCOEFF_NORMED
    match = cv2.matchTemplate(screenshot, template, method)
    _, confidence_result, _, max_locate = cv2.minMaxLoc(match)

    if confidence_result < confidence:
        raise ValueError(
            f"Confidence matching was below the threshold. Obtained: {confidence_result:.2f}, Expected: {confidence:.2f}."
        )

    template_width, template_height = template.shape[::-1]
    return (
        max_locate[0] + template_width // 2,
        max_locate[1] + template_height // 2,
        template_width,
        template_height,
    )


def read_image(image_path: str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError(f"Failed to load image at path: {image_path}")

    return image
