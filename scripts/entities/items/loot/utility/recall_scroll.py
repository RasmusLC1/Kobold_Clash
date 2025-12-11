from scripts.entities.items.loot.utility.utility_loot import Utility_Loot
from scripts.engine.keys.keys import keys

class Recall_Scroll(Utility_Loot):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, type, pos, 320, amount, rarity_value)
        self.Set_Description()

    def Set_Description(self):
        self.description = 'Teleport back\nto latest shrine'

    # Handle reset normally in case item that increases use of other items
    def Reset_Scroll(self):
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
        
        self.Teleport_To_Shrine()

    
    # Effect of opening door on key
    def Teleport_To_Shrine(self):
        player = self.game.player
        if not player.last_shrine_visited:
            return False
        player.Set_Position(player.last_shrine_visited.pos.copy())
        self.Reset_Scroll()
        self.game.sound_handler.Play_Sound(self.type, 1)
        return True

    def Render_Line(self, surf, offset, alpha):
        pass
