from scripts.entities.items.loot.loot import Loot
import pygame
from scripts.engine.keys.keys import keys

class Recipe_Scroll(Loot):
    def __init__(self, game, pos):
        super().__init__(game, keys.recipe_scroll, pos, (16, 16), 10, keys.passive)
        self.update_cooldown = 0
        self.potion_IDs = []
        self.description = 'Improves\nefficiency\nof potions'


    def Update(self, delta_time):
        if self.update_cooldown:
            self.update_cooldown -= delta_time
        else:
            self.update_cooldown = 8
            self.Check_Loot_In_Inventory()
            
            
        return super().Update(delta_time)
    
    def Check_Loot_In_Inventory(self):
        inventory_loot = self.game.inventory.item_inventory.Find_Loot()

        for item in inventory_loot:
            if item.sub_category != keys.loot:
                print("WRONG Item type added to Recipe Scroll", item)
                continue
            if item.ID in self.potion_IDs:
                continue
            
            if item.loot_type != keys.potion:
                continue

            # Item is verified to be a potion
            item.Increase_Strength() 
            self.potion_IDs.append(item.ID)


    # TODO: MAKE a red overlay for item
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
        # Render on Mouse position as the item position is not being updated
        # surf.blit(self.entity_image, (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1]))

    def Place_Down(self):
        self.Delete_Item()