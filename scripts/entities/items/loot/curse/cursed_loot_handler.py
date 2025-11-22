

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

    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = None):
        if not type:
            type, amount = self.Get_Loot_Based_On_Rarity(rarity_value)
        loot_class = self.loot_map.get(type)
        if not loot_class:
            return None
        
        loot = loot_class(self.game, type, pos, amount, rarity_value)

        return loot


    def Get_Loot_Values(self):
        loot_types_cost = {
            keys.black_coin : 30,
            keys.temptress_embrace : 25,
            keys.demonic_bargain : 25,
            keys.blood_tomb : 25,
        }
        return loot_types_cost
