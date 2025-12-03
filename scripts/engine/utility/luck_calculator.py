import random

class Luck_Calculator():
    def Get_Loot_Based_On_Rarity(rarity_value, loot_types_cost):
        valid_items  = Luck_Calculator.Get_Valid_Items(rarity_value, loot_types_cost)

        if not valid_items:
            return None, 0

        weights = Luck_Calculator.Set_Weights(valid_items)

        # Weighted random choice
        chosen_loot_type, chosen_cost = random.choices(valid_items, weights=weights, k=1)[0]

        amount = rarity_value // chosen_cost
        return chosen_loot_type, amount
        
    def Get_Loot_Values():
        pass


    def Get_Valid_Items(rarity_value, loot_types_cost):
        
        if not loot_types_cost:
            return None

        # Filter valid items
        valid_items = [(name, cost) for name, cost in loot_types_cost.items() if cost <= rarity_value]

        return valid_items

    # Weight rare items more as rarity_value increases
    def Set_Weights(valid_items):
        weights = []
        for name, cost in valid_items:
            # Higher cost ⇒ larger weight
            # Lower cost ⇒ less weight
            weight = max(1, cost)  
            weights.append(weight)

        return weights