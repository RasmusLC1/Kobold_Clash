from scripts.entities.items.loot.valueable.gold import Gold
from scripts.entities.items.loot.valueable.hunter_treasure import Hunter_Treasure 
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys

# Handle valuables uniquely since gems and ingots have a large pool of potential items
class Valuable_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)


        self.loot_map = {
            keys.gold: Gold,
            keys.hunter_treasure: self.Spawn_Hunter_Treasure
        }

        self.loot_types_cost = {
            keys.gold : 1,
        }


    def Spawn_Hunter_Treasure(self, pos, amount = 0, type = None):
        loot = Hunter_Treasure(self.game, pos)
        return loot


    def Get_Loot_Values(self):

        return self.loot_types_cost
