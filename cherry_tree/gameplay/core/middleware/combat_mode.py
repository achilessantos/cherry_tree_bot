from cherry_tree.repositories.combat_window.core import get_combat_mode

# from ...typings import Context


def set_combat_mode_middleware(context, combat_mode):
    context["combat"]["strength"]["enabled"] = get_combat_mode(context["screenshot"], combat_mode)

    return context
