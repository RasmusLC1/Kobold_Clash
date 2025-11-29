from scripts.entities.items.loot.utility.utility_loot import Utility_Loot
import random
from scripts.engine.keys.keys import keys

class Shadow_Cloak(Utility_Loot):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, type, pos, 320, amount, rarity_value)
        self.Set_Description()

    def Set_Description(self):
        self.description = 'Become\ninvisibile'

    # When cloak runs out of charges it's deleted
    def Reset_Cloak(self):
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
        
        self.Activate_Invisibility()

    
    # Effect of opening door on key
    def Activate_Invisibility(self):
        self.game.player.Set_Effect(keys.invisibility, 5)
        self.Reset_Cloak()

    def Render_Line(self, surf, offset, alpha):
        pass