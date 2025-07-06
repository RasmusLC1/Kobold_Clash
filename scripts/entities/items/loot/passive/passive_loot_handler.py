
from scripts.entities.items.loot.passive.lantern import Lantern
from scripts.entities.items.loot.passive.passive_loot import Passive_Loot
from scripts.entities.items.loot.passive.echo_sigil import Echo_Sigil
from scripts.entities.items.loot.passive.recipe_scroll import Recipe_Scroll
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler

import random
from scripts.engine.keys.keys import keys


class Passive_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

        self.loot_map = {
            keys.lantern: Lantern,
            keys.echo_sigil: Echo_Sigil,
            keys.recipe_scroll: Recipe_Scroll,
            keys.anchor_stone : Passive_Loot,
            keys.magnet : Passive_Loot,
            keys.strength_totem : Passive_Loot,
            keys.power_totem : Passive_Loot,
            keys.muffled_boots : Passive_Loot,
            keys.halo : Passive_Loot,
            keys.faith_pendant : Passive_Loot,
            keys.lucky_charm : Passive_Loot,
        }

        self.special_type = [
            keys.lantern,
            keys.echo_sigil,
            keys.recipe_scroll,
        ]


    def Loot_Spawner(self, pos, type = None, amount = None):
        if not type:
            type = random.choice(list(self.loot_map.keys()))
        loot = None
        if type in self.special_type: # Handle lantern seperately as it needs light updates
            loot_class = self.loot_map.get(type)
            if not loot_class:
                return None
            

            loot = loot_class(self.game, pos)
        else:
            loot = Passive_Loot(self.game, type, pos)


        return loot




