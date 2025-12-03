from scripts.entities.items.loot.valueable.gold import Gold
from scripts.entities.items.loot.valueable.gem import Gem
from scripts.entities.items.loot.valueable.hunter_treasure import Hunter_Treasure 
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys
from scripts.engine.utility.luck_calculator import Luck_Calculator

import random

GOLD_COST = 3
MIN_GEM_VALUE = 5

# Handle valuables uniquely since gems and ingots have a large pool of potential items
class Valuable_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)


        self.loot_map = {
            keys.gold: self.Spawn_Gold,
            keys.gem: self.Spawn_Gem,
            keys.hunter_treasure: self.Spawn_Hunter_Treasure
        }

    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = None):
        if not type:
            type, amount = self.Get_Loot_Based_On_Rarity(rarity_value)
        loot_class = self.loot_map.get(type)
        if not loot_class:
            return None
        
        try:
            loot = loot_class(pos, amount, rarity_value)
            self.game.item_handler.Add_Item(loot)
        except Exception as e:
            print(f"Failed to spawn loot{e}", type, pos, amount, rarity_value, loot_class)
            return

        return loot
    
    def Get_Loot_Based_On_Rarity(self, rarity_value):
        valid_items  = self.Get_Valid_Items(rarity_value)

        if not valid_items:
            return None, 0

        weights = Luck_Calculator.Set_Weights(valid_items)

        # Weighted random choice
        chosen_loot_type, chosen_cost = random.choices(valid_items, weights=weights, k=1)[0]

        amount = rarity_value // chosen_cost
        return chosen_loot_type, amount

    def Spawn_Gold(self, pos, amount = 1, rarity_value = 1):
        amount *= GOLD_COST # offset the gold cost used for weights
        loot = Gold(self.game, pos, int(amount))
        return loot

    
    def Spawn_Gem(self, pos, amount, rarity_value):

        valid_item = self.Get_Valid_Items(rarity_value, self.Get_Gem_Values())
        weights = Luck_Calculator.Set_Weights(valid_item)

        chosen_loot_type, chosen_cost = random.choices(valid_item, weights=weights, k=1)[0]
        amount = rarity_value // chosen_cost
        print(amount, rarity_value, chosen_cost)
        effect = chosen_loot_type.split("_g")[0] # Use _g to prevent failure at multi word gems like increase_strength

        loot = Gem(self.game, pos, int(amount), effect, chosen_cost)
        return loot


    def Get_Valid_Items(self, rarity_value, function=None):

        # Use default if no function was passed
        if function is None:
            function = self.Get_Loot_Values()

        loot_types_cost = function

        if not loot_types_cost:
            return None

        valid_items = [(name, cost) for name, cost in loot_types_cost.items()
                    if cost <= rarity_value]

        return valid_items


    def Spawn_Hunter_Treasure(self, pos, amount = 0, type = None):
        loot = Hunter_Treasure(self.game, pos)
        return loot

    def Get_Gem_Values(self):
        gems = {
            keys.fire_gem : 10,
            keys.frozen_gem : 10,
            keys.electric_gem : 10,
            keys.poison_gem : 10,
            keys.vampiric_gem : 30,
            keys.arcane_hunger : 30,
            keys.blunt_gem : MIN_GEM_VALUE,
            keys.slash_gem : MIN_GEM_VALUE,
            keys.halo_gem : 40,
            keys.power_gem : 30,
            keys.range_gem : 10,
            keys.speed_gem : 10,
            keys.strength_gem : 10,
            keys.terror_gem : 40,
            keys.vulnerable_gem : 20,
            keys.weakness_gem : 20,
            keys.wet_gem : 10,
            keys.durability_gem : 10,
        }
        return gems
    

    def Get_Loot_Values(self):
        loot_types_cost = {
            keys.gold : GOLD_COST,
            keys.gem : MIN_GEM_VALUE,
        }

        return loot_types_cost
