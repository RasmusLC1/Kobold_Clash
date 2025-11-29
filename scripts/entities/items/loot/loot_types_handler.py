from scripts.engine.keys.keys import keys
import random


class Loot_Types_Handler():
    def __init__(self, game):
        self.game = game    

        self.loot_map = {}


    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = None):
        if not type:
            type, amount = self.Get_Loot_Based_On_Rarity(rarity_value)
        loot_class = self.loot_map.get(type)
        if not loot_class:
            return None
        
        try:
            loot = loot_class(self.game, type, pos, amount, rarity_value)
            self.game.item_handler.Add_Item(loot)
        except Exception as e:
            print(f"Failed to spawn loot{e}", type, pos, amount, rarity_value, loot_class)

        return loot

    def Get_Loot_Based_On_Rarity(self, rarity_value):
        valid_items  = self.Get_Valid_Items(rarity_value)

        if not valid_items:
            return None, 0

        weights = self.Set_Weights(valid_items)

        # Weighted random choice
        chosen_loot_type, chosen_cost = random.choices(valid_items, weights=weights, k=1)[0]

        if chosen_loot_type == keys.gold:
            chosen_cost = 1

        amount = rarity_value // chosen_cost
        return chosen_loot_type, amount
    
    def Get_Loot_Values(self):
        pass

    def Get_Valid_Items(self, rarity_value):
        
        loot_types_cost = self.Get_Loot_Values()

        if not loot_types_cost:
            return None

        # Filter valid items
        valid_items = [(name, cost) for name, cost in loot_types_cost.items() if cost <= rarity_value]

        return valid_items

    # Weight rare items more as rarity_value increases
    def Set_Weights(self, valid_items):
        weights = []
        for name, cost in valid_items:
            # Higher cost ⇒ larger weight
            # Lower cost ⇒ less weight
            weight = max(1, cost)  
            weights.append(weight)

        return weights

