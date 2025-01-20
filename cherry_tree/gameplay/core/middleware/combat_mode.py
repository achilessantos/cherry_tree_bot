from cherry_tree.repositories.combat_window.core import get_combat_mode

# from ...typings import Context


def set_combat_mode_middleware(context):
    return get_combat_mode(context["gameWindow"]["name"])
