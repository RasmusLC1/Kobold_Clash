

from scripts.entities.items.loot.curse.cursed_loot import Cursed_Loot
from scripts.entities.items.loot.curse.black_coin import Black_Coin
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler

import random
from scripts.engine.keys.keys import keys


class Cursed_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

        self.loot_map = {
            keys.black_coin: Black_Coin,
            keys.temptress_embrace : Cursed_Loot,
            keys.demonic_bargain : Cursed_Loot,
            keys.blood_tomb : Cursed_Loot,
        }

        # Needs special spawning conditions
        self.special_type = [
            keys.black_coin,
        ]



    def Loot_Spawner(self, pos, rarity_value, type = None, amount = None):
        if not type:
            type = random.choice(list(self.loot_map.keys()))
        loot = None
        if type in self.special_type: # Handle lantern seperately as it needs light updates
            loot_class = self.loot_map.get(type)
            if not loot_class:
                return None
            

            loot = loot_class(self.game, pos)
        else:
            loot = Cursed_Loot(self.game, type, pos)


        return loot




