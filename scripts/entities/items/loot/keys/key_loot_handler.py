from scripts.entities.items.loot.keys.skeleton_key import Skeleton_Key
from scripts.entities.items.loot.keys.blood_key import Blood_Key
from scripts.entities.items.loot.keys.soul_key import Soul_Key
from scripts.entities.items.loot.keys.cursed_key import Cursed_Key
from scripts.entities.items.loot.keys.lockpick import Lockpick
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys



class Key_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)


        self.loot_map = {
            keys.skeleton_key: Skeleton_Key,
            keys.blood_key: Blood_Key,
            keys.soul_key: Soul_Key,
            keys.cursed_key: Cursed_Key,
            keys.lockpick: Lockpick,
        }

        self.loot_types_cost = {
            # Skeleton Key – Unlocks any door but disappears after 1 use.
            keys.skeleton_key: 10,

            # Blood Key – Unlocks any door but costs health.
            keys.blood_key: 15,

            # Soul Key – Unlocks any door but costs souls.
            keys.soul_key: 15,

            # Cursed Key – Unlocks any door but gives a random curse.
            keys.cursed_key: 15,

            # Lockpick – has a 1/3chance to open the door and persist, high clatter on fail
            keys.lockpick: 10,
        }

