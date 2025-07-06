from scripts.entities.items.loot.loot import Loot
import pygame
from scripts.engine.keys.keys import keys

class Echo_Sigil(Loot):
    def __init__(self, game, pos):
        super().__init__(game, keys.echo_sigil, pos, (16, 16), 10, keys.passive)
        self.update_cooldown = 0
        self.loot_IDs = []
        self.description = 'Grants\nextra use\nto items\n'


    def Update(self):
        if self.update_cooldown:
            self.update_cooldown -= 1
        else:
            self.update_cooldown = 500
            self.Check_Loot_In_Inventory()
            
            
        return super().Update()
    
    def Check_Loot_In_Inventory(self):
        inventory_loot = self.game.inventory.item_inventory.Find_Loot()

        for item in inventory_loot:
            if item.sub_category != keys.loot:
                print("WRONG Item type added to Echo Sigil", item)
                continue
            if item.ID in self.loot_IDs:
                continue
            
            # Increase amount for multi use utility items by checking amount since
            # utility items shouldn't have more than 10 uses
            if item.max_amount > 1 and item.max_amount < 10:
                item.Increase_Amount(1)
            self.loot_IDs.append(item.ID)

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