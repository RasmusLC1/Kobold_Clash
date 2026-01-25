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
    
    
    def Calculate_Rarity_Value(game, min_rarity_value = None, max_rarity_value = None, clamp_values = True):
        # Depth 0–7 → 0–30
        depth_factor = (game.depth / 7) * 30

        # Luck 0–10 → 0–30
        luck_factor = (game.player.luck / 10) * 30

        # Clatter 0–10 → 0–30
        clatter_factor = (game.clatter.Get_Awakening_Level() / 10) * 30

        # Swing randomness (rare bumps/dips): -10 to +10
        swing = random.uniform(-15, 15)
        total_rarity = max(1, int(depth_factor + luck_factor + clatter_factor + swing))

        if not clamp_values:
            return total_rarity
        
        return Luck_Calculator.Clamp_Rarity(total_rarity, min_rarity_value, max_rarity_value)
    
    
    # Clamp the rarity value to prevent legendaries from dropping in vases
    def Clamp_Rarity(rarity_value, min_rarity_value, max_rarity_value):
        return max(min_rarity_value, min(max_rarity_value, rarity_value))


