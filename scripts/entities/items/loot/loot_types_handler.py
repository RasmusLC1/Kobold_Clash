from scripts.engine.keys.keys import keys
import random


class Loot_Types_Handler():
    def __init__(self, game):
        self.game = game    

        self.loot_map = {}



    def Loot_Spawner(self, pos, rarity_value, type = None, amount = None):
        if not type:
            type = random.choice(list(self.loot_map.keys()))
        loot_class = self.loot_map.get(type)
        if not loot_class:
            return None
        

        loot = loot_class(self.game, pos)

        return loot
