import logging
from cherry_tree.gameplay.core.tasks.orchestrator.base import BaseTask
from cherry_tree.gameplay.core.tasks.orchestrator.task_status import TaskStatus
from cherry_tree.gameplay.typings import Context
from cherry_tree.repositories.combat_window.core import get_combat_mode, set_combat_mode


logger = logging.getLogger("main")
DEFAULT_COMBAT_MODE = "strength"


class SetCombatModeTask(BaseTask):
    def __init__(self):
        super().__init__(
            name="set_combat_mode",
            delay_before_start=0.5,
            delay_after_complete=0.5,
        )

    def execute(self, context: Context) -> Context:
        get_combat_mode_enabled = self.get_combat_mode_enabled(context)

        if get_combat_mode_enabled:
            self.status = TaskStatus.COMPLETED.value
            return context

        coordinate = get_combat_mode(context["screenshot"])

        if coordinate:
            set_combat_mode(coordinate)
            logger.info(f"Combat mode {DEFAULT_COMBAT_MODE} was selected!")
            context["combat"]["strength"]["enabled"] = True
            self.status = TaskStatus.COMPLETED.value

        return context

    def get_combat_mode_enabled(self, context: Context):
        enabled_combat_types = []

        for combat_type, settings in context["combat"].items():
            if settings.get("enabled"):
                enabled_combat_types.append(combat_type)

        if len(enabled_combat_types) == 1:
            return enabled_combat_types[0]

        return None
