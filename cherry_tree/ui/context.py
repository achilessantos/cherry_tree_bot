from genericpath import exists
from tinydb import Query, TinyDB
from cherry_tree.gameplay.core.load import load_context_from_config

GAME_WINDOW_NAME = "CherryTree - Text RPG"


class Context:
    file_path: str = "profile.json"

    def __init__(self, context):
        should_insert_profile = not exists(self.file_path)
        self.db = TinyDB(self.file_path)
        if should_insert_profile:
            self.insert_profile()
        self.enabled_profile = self.get_enabled_profile()
        self.context = load_context_from_config(self.enabled_profile["config"], context)

    def insert_profile(self):
        self.db.insert(
            {
                "enabled": True,
                "config": {
                    "combat": {
                        "attack": {"enabled": False, "image": None},
                        "defense": {"enabled": False, "image": None},
                        "distance": {"enabled": False, "image": None},
                        "strength": {"enabled": False, "image": None},
                    },
                    "gameWindow": {"name": GAME_WINDOW_NAME},
                    "slayerHunting": {
                        "enabled": False,
                        "slayerLevel": None,
                        "slayerCreature": None,
                    },
                },
            }
        )

    def get_enabled_profile(self):
        return self.db.search(Query().enabled == True)[0]
