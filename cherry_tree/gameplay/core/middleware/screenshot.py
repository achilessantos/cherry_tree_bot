from cherry_tree.utils.core import get_screenshot
from ...typings import Context

def set_screenshot_middleware(context: Context) -> Context:
    context['screenshot'] = get_screenshot()

    return context