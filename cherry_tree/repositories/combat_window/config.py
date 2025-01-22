from pathlib import Path


absolute_path = Path(__file__).parent.resolve()
root_dir = Path.cwd()
relative_path = absolute_path.relative_to(root_dir)
images_path = f"{relative_path}\\images"
combat_mode_path = f"{images_path}\\combat_mode"
buttons_path = f"{images_path}\\buttons"
messages_path = f"{images_path}\\messages"
images = {
    "combatMode": {
        "attack_mode": f"{combat_mode_path}\\attack_mode.png",
        "defense_mode": f"{combat_mode_path}\\defense_mode.png",
        "strength_mode": f"{combat_mode_path}\\strength_mode.png",
        "unchecked_attack_mode": f"{combat_mode_path}\\unchecked_attack_mode.png",
        "unchecked_defense_mode": f"{combat_mode_path}\\unchecked_defense_mode.png",
        "unchecked_distance_mode": f"{combat_mode_path}\\unchecked_distance_mode.png",
        "unchecked_strength_mode": f"{combat_mode_path}\\unchecked_strength_mode.png",
    },
    "buttons": {
        "collectLoots": f"{buttons_path}\\collectLoots.png",
        "leave": f"{buttons_path}\\leave.png",
        "menu": f"{buttons_path}\\menu.png",
        "potionMenu": f"{buttons_path}\\potionMenu.png",
    },
    "messages": {
        "searchingForEnemy": f"{messages_path}\\searchingForEnemy.png",
        "slayerKillsLeft": f"{messages_path}\\slayerKillsLeft.png",
    },
}
