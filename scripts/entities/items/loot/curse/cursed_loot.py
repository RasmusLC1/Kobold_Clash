from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys
import pygame

# Generic passive loot that changes depending on the type, simplified to one
# class since it uses effects
class Cursed_Loot(Loot):
    def __init__(self, game, type, pos, effect_power, value):
        super().__init__(game, type, pos, (16, 16), 10, keys.passive)

    def Pick_Up(self):
        if not super().Pick_Up():
            return False
        
        self.game.player.inventory_effects.Enable(self.type)
        return True

    def Place_Down(self):
        if not super().Place_Down():
            return False
        
        self.game.player.inventory_effects.Disable(self.type)
        return True

        

      # # Render item with fadeout if it's in an illegal position
    def Render_In_Bounds(self, player_pos, mouse_pos, surf, offset = (0,0)):
         # Copy image and set alpha
        entity_image =  pygame.transform.scale(self.entity_image.copy(), self.floor_size)
        # entity_image.set_alpha(255)

        # Create red overlay
        red_overlay = pygame.Surface(entity_image.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 100))  # Red with transparency

        # Blit entity and red overlay
        pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
        surf.blit(entity_image, pos)
        surf.blit(red_overlay, pos)

    def Place_Down(self):
        self.Delete_Item()
