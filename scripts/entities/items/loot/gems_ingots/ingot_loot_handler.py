from scripts.entities.items.loot.gems_ingots.ingot import Ingot
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys


class Ingot_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

        self.loot_types_cost = {
            keys.Steel_ingot: 25,
            keys.jade_ingot: 25,
            keys.copper_ingot: 30,
            keys.Gold_ingot: 40,
            keys.Silver_ingot: 45,
        }

        self.loot_map = {ingot_type: Ingot for ingot_type in self.loot_types_cost}