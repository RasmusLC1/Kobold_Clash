import pygame
from scripts.engine.keys.keys import keys
from scripts.interface.inventory.inventory_slot import Inventory_Slot

class Weapon_Inventory_Slot(Inventory_Slot):
    def __init__(self, game, pos, type, size, item, index, key = None):
        super().__init__(game, pos, type, size, item, index, key)
        self.active_inventory = False
         

    # Set state to active
    def Set_Active_Inventory(self):
        self.active_inventory = True
        self.border_color = (255,215,0) # Gold

    # Remove active state
    def Remove_Active_Inventory(self):
        self.active_inventory = False
        self.border_color = (0, 0, 0) # Black

    def Render(self, surf):
        if self.active_inventory:
            gold = (255,215,0)
            pygame.draw.rect(surf, gold, self.rect(), 1)
            
        return super().Render(surf)

    # Render the keyboard shortcut
    def Render_Key(self, surf):
        pass