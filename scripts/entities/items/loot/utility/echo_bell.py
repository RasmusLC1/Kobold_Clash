from scripts.entities.items.loot.utility.utility_loot import Utility_Loot
import random
from scripts.engine.keys.keys import keys

class Echo_Bell(Utility_Loot):
    def __init__(self, game, pos):
        amount = random.randint(2, 4)
        super().__init__(game, keys.echo_bell, pos, 320, amount)
        self.Set_Description()
        self.max_amount = 5

    def Set_Description(self):
        self.description = 'Lure enemies\nto a location'


    def Reset_Bell(self):
        self.amount -= 1
        if self.amount:
            self.clicked = False
            self.Set_Description() # Update description
            return
        
        self.game.item_handler.Remove_Item(self, True)
        self.game.inventory.Remove_Item(self)
    
    # The update function in the inventory
    def Update_In_Inventory(self):
        if not super().Update_In_Inventory():
            return False
        
        if self.game.mouse.left_click:
            self.Toll_Bell()

    

    # Effect of opening door on key
    def Toll_Bell(self):
        self.game.clatter.Generate_Clatter(self.game.mouse.mpos, 1000) # Generate clatter to alert enemies
        self.Reset_Bell()

        self.game.sound_handler.Play_Sound('bell', 0.5, self.game.mouse.mpos)

