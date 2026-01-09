

from scripts.entities.items.loot.curse.cursed_loot import Cursed_Loot
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler

import random
from scripts.engine.keys.keys import keys


class Cursed_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

        self.loot_map = {
            keys.black_coin: Cursed_Loot,
            keys.temptress_embrace : Cursed_Loot,
            keys.demonic_bargain : Cursed_Loot,
            keys.blood_tomb : Cursed_Loot,
            keys.blood_ring : Cursed_Loot,
            keys.forsaken_grimoire : Cursed_Loot,
        }

  


    def Get_Loot_Values(self):
        loot_types_cost = {
            # Increases gold, but increases damage taken
            keys.black_coin : 15,

            # # Increases damage when health when low
            # keys.temptress_embrace : 15,

            # # Scales damage but prevent healing
            # keys.demonic_bargain : 25,

            # # Gain souls when damaged
            # keys.blood_tomb : 20,

            # # Powerful life steal but slowly drains you
            # keys.blood_ring : 30,

            # Improves runes but reduces strength
            keys.forsaken_grimoire : 10, 
        }
        print(self.game.player.luck)
        return loot_types_cost
