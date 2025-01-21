from cherry_tree.repositories.game_window.core import is_activated_game_window

# from ...typings import Context


def set_game_window_middleware(context):
    if context["gameWindow"]["enabled"]:
        return context

    context["gameWindow"]["enabled"] = is_activated_game_window(
        context["gameWindow"]["name"]
    )

    return context
