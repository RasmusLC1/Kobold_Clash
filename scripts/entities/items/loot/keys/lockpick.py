from scripts.entities.items.loot.keys.key import Key
import random
from scripts.engine.keys.keys import keys
import math


class Lockpick(Key):
    def __init__(self, game, type, pos, amount, rarity_value):
        self.chance_to_break = amount
        super().__init__(game, keys.lockpick, pos, rarity_value)


    def Set_Description(self):
        self.description = f'{self.Calculate_Succes_Chance()}% chance\nto persist'


    def Open_Door(self):
        if self.Check_If_persist():
            return True
        
        game = self.game # cache game for quick lookup
        game.inventory.Remove_Item(self)
        game.item_handler.Remove_Item(self, True)
        game.clatter.Generate_Clatter(self.pos, 1000) # Generate extra clatter for failure
        return True
    

    def Check_If_persist(self):
        
        success_rate_percent = self.Calculate_Succes_Chance()
        # Generate a random number from 1 to 100
        roll = random.randint(1, 100)
        
        # Check for success (if the roll is within the success range)
        if roll <= success_rate_percent:
            # Item persists/doesn't break
            return True
        
    
    def Calculate_Succes_Chance(self):
        min_success_percent = 10
        max_success_percent = 95
        max_amount = 10
        min_amount = 1
        
        # Calculate the base success rate (linear interpolation)
        # Success_Range = 95 - 10 = 85
        # Amount_Range = 10 - 1 = 9
        # Per_Level_Increase = 85 / 9 = 9.4
        
        # Calculate the final success percentage
        success_rate_percent = min_success_percent + (self.chance_to_break - min_amount) * (
            (max_success_percent - min_success_percent) / (max_amount - min_amount)
        )
        return math.ceil(success_rate_percent)