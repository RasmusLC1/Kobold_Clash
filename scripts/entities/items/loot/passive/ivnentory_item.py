from scripts.entities.items.loot.loot import Loot
import pygame
from scripts.engine.keys.keys import keys

# Grants extra use to items
class Inventory_Item(Loot):
    def __init__(self, game, type, pos, effect_power, rarity_value):
        self.effect_power = int(effect_power)
        super().__init__(game, type, pos, (16, 16), rarity_value, keys.passive)
        self.update_cooldown = 0
        self.loot_IDs = []


    def Update(self, delta_time):
        if self.update_cooldown:
            self.update_cooldown -= delta_time
        else:
            self.update_cooldown = 5 # Check every 5 seconds
            self.Check_Loot_In_Inventory()
            
            
        return super().Update(delta_time)
    
    def Check_Loot_In_Inventory(self):
        pass

    def Place_Down(self):
        if self.game.decoration_handler.Check_Item_Collision(self):
            return None
        
        inventory_loot = self.game.inventory.item_inventory.Find_Loot()

        return inventory_loot
    


    # # Render item with fadeout if it's in an illegal position
    def Render_In_Bounds(self, player_pos, mouse_pos, surf, offset = (0,0)):
         # Copy image and set alpha
        entity_image = self.entity_image.copy()
        # entity_image.set_alpha(255)

        # Create red overlay
        red_overlay = pygame.Surface(entity_image.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 100))  # Red with transparency

        # Blit entity and red overlay
        pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
        surf.blit(entity_image, pos)
        surf.blit(red_overlay, pos)
