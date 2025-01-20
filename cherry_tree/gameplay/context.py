""""
Gameplay context that be passed and modified by program until its running, all action that be used
on bot needs to be configured here.
"""

CONTEXT = {
    "combat": {
        "attack": {"enabled": False, "image": None},
        "defense": {"enabled": False, "image": None},
        "distance": {"enabled": False, "image": None},
        "strength": {"enabled": False, "image": None},
    },
    "gameWindow": {"enabled": None, "name": None},
    "pause": False,
    "slayerHunting": {"enabled": True, "slayerLevel": None, "slayerCreature": None},
}
