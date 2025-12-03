from scripts.engine.utility.luck_calculator import Luck_Calculator


class Loot_Types_Handler():
    def __init__(self, game):
        self.game = game    
        self.loot_map = {}


    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = None):
        if not type:
            type, amount = Luck_Calculator.Get_Loot_Based_On_Rarity(rarity_value, self.Get_Loot_Values())
        loot_class = self.loot_map.get(type)
        if not loot_class:
            return None
        
        try:
            loot = loot_class(self.game, type, pos, amount, rarity_value)
            self.game.item_handler.Add_Item(loot)
        except Exception as e:
            print(f"Failed to spawn loot{e}", type, pos, amount, rarity_value, loot_class)
            return

        return loot


    def Get_Loot_Values(self):
        pass