from scripts.entities.items.loot.utility.echo_bell import Echo_Bell
from scripts.entities.items.loot.utility.shadow_cloak import Shadow_Cloak
from scripts.entities.items.loot.utility.faded_hourglass import Faded_Hourglass
from scripts.entities.items.loot.utility.ethereal_chains import Ethereal_Chains
from scripts.entities.items.loot.utility.recall_scroll import Recall_Scroll
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys


class Utility_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)


        self.loot_map = {
            keys.echo_bell: Echo_Bell,
            keys.faded_hourglass : Faded_Hourglass,
            keys.ethereal_chains : Ethereal_Chains,
            keys.shadow_cloak: Shadow_Cloak,
            keys.recall_scroll: Recall_Scroll,
        }


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