import random
from scripts.engine.keys.keys import keys
from scripts.engine.utility.luck_calculator import Luck_Calculator

class LootComponent:
    def __init__(self, game, entity_type, min_rarity, max_rarity, loot_weights=None):
        self.game = game
        self.type = entity_type
        self.min_rarity = min_rarity
        self.max_rarity = max_rarity
        self.loot_weights = loot_weights or {}
        self.empty = False

    def Drop_Loot(self, pos, multiplier=1):
        if self.empty:
            return
            
        rarity_value = self.Calculate_Rarity(multiplier)
        loot_type = self.Calculate_Loot_Type(rarity_value)

        if loot_type != keys.nothing:
            self.game.item_handler.Spawn_Item_By_Type(loot_type, pos, rarity_value=rarity_value)
            
        self.empty = True
        self.game.item_handler.Reset_Nearby_Items_Cooldown()

    def Calculate_Rarity(self, multiplier):
        min_val = self.min_rarity * max(1, multiplier)
        max_val = self.max_rarity * max(1, multiplier)
        return Luck_Calculator.Calculate_Rarity_Value(self.game, min_val, max_val)

    def Calculate_Loot_Type(self, rarity_value):
        if not self.loot_weights:
            return keys.nothing
            
        affordable = self.game.item_handler.Check_If_Loot_Is_Affordable(
            list(self.loot_weights.keys()), rarity_value
        )
        if not affordable:
            return keys.nothing
            
        weights = [self.loot_weights[t] for t in affordable]
        return random.choices(affordable, weights, k=1)[0]