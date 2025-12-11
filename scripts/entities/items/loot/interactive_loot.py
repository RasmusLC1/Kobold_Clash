from scripts.entities.items.loot.loot import Loot
import math
import pygame
from scripts.engine.keys.keys import keys

class Interactive_Loot(Loot):
    def __init__(self, game, type, pos, max_distance, size, loot_type, rarity_value, amount, max_amount = 3):
        super().__init__(game, type, pos, size, rarity_value=rarity_value, loot_type=loot_type, amount=amount, max_amount = max_amount)
        self.distance_to_player = 0
        self.max_distance = max_distance

    def Update(self, delta_time):
        if self.game.mouse.right_click:
            self.clicked = False

        return super().Update(delta_time)

    def Calculate_Distance_To_Player(self):
        player_pos = self.game.player.pos
        mpos = self.game.mouse.mpos
        self.distance_to_player = math.sqrt((player_pos[0] - mpos[0]) ** 2 + (player_pos[1] - mpos[1]) ** 2)

    def Activate(self):
        if not super().Activate():
            return
        self.clicked = True

    # The update function in the inventory
    def Update_In_Inventory(self):
        if not self.clicked:
            return False
        
        # Set range limit for the key
        self.Calculate_Distance_To_Player()
        if self.distance_to_player > self.max_distance:
            return False
        
        return True
        


    def Render_Active(self, surf, offset = (0,0)):
        if not self.clicked:
            return False
        rendered_image = self.entity_image.copy()

        alpha = 160

        # Fade the key out if distance is to great
        if self.distance_to_player > self.max_distance:
            alpha = 50
            rendered_image.set_alpha(alpha)
        
        self.Render_Line(surf, offset, alpha)
        mpos = self.game.mouse.mpos
        surf.blit(rendered_image, (mpos[0] - offset[0] - 10, mpos[1] - offset[1] - 5))
        return

    def Render_Line(self, surf, offset, alpha):
        # Create a transparent surface for the line
        line_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        
        light_grey = (211, 211, 211, alpha)
        player_pos_offset = (self.game.player.rect().center[0] - offset[0], self.game.player.rect().center[1] - offset[1])
        mouse_pos_offset = (self.game.mouse.player_mouse[0] - offset[0], self.game.mouse.player_mouse[1] - offset[1])

        pygame.draw.line(line_surf, light_grey, player_pos_offset, mouse_pos_offset, 2)  

        surf.blit(line_surf, (0, 0))  # No blending needed
