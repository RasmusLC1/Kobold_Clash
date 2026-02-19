from scripts.engine.utility.luck_calculator import Luck_Calculator


class Loot_Types_Handler():
    def __init__(self, game):
        self.game = game    
        self.loot_map = {}
        self.loot_types_cost = {}


    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = 1):
        if not type:
            type, amount, value = Luck_Calculator.Get_Loot_Based_On_Rarity(rarity_value, self.Get_Loot_Values())
        else:
            value = rarity_value
        loot_class = self.loot_map.get(type)
        if not loot_class:
            return None
        
        try:
            loot = loot_class(self.game, type, pos, amount, value)
            self.game.item_handler.Add_Item(loot)
        except Exception as e:
            print(f"Failed to spawn loot{e}", type, pos, amount, value, loot_class)
            return

        return loot
    

    def Get_Lowest_Value(self, rarity_value):
        min_cost = min(self.Get_Loot_Values().values())
        return rarity_value > min_cost


    def Get_Loot_Values(self):
        return self.loot_types_cost