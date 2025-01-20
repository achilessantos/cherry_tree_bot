from cherry_tree.utils.window import restore_window


def active_game_window(context):
    if context["gameWindow"]["enabled"]:
        return context

    restore_window(context["gameWindow"]["name"])
    context["gameWindow"]["enabled"] = True

    return context
