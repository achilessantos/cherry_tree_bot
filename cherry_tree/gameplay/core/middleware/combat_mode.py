from cherry_tree.gameplay.typings import Context
from cherry_tree.repositories.combat_window.core import get_combat_mode


def set_combat_mode_middleware(context: Context, combat_mode) -> Context:
    context["combat"]["strength"]["enabled"] = get_combat_mode(
        context["screenshot"], combat_mode
    )

    return context
