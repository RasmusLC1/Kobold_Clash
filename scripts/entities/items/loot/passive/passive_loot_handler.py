
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


    def Get_Loot_Values(self):
        loot_types_cost = {
            # Echo Bell – Creates a noise at a targeted location to lure enemies away.
            keys.echo_bell: 20,
            # Faded Hourglass – Slows down nearby enemies movement.
            keys.faded_hourglass: 30,
            # Ethereal Chains – Snares nearby enemies for a short duration.
            keys.ethereal_chains: 50,
            # Cloak of Shadows – Temporarily makes the player invisible to enemies.
            keys.shadow_cloak: 50,
            # Recall Parchment – Teleports the player back to the last shrine visited.
            keys.recall_scroll: 20,
        }

        return loot_types_cost





