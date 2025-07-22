from scripts.engine.keys.keys import keys
from scripts.interface.ui.ui import UI
import math
import pygame

class Souls(UI):
    def __init__(self, game):
        pos_x = game.screen_width // game.render_scale - 50
        pos_y = 40
        animation_max = 3
        animation_cooldown_max = 0.3
        super().__init__(game, pos_x, pos_y, animation_max, animation_cooldown_max)
        self.stored_souls = -99999
        self.base_x = pos_x


    def Update(self, delta_time):
        super().Update(delta_time)
        self.move_text_based_on_soul()


    def move_text_based_on_soul(self):

        if self.stored_souls == self.game.player.souls:
            return
        self.stored_souls = self.game.player.souls
        # Get the number of digits in the soul count
        num_digits = math.floor(math.log10(self.stored_souls)) + 1 if self.stored_souls > 0 else 1
        
        # Calculate the new position by moving 8 pixels left per extra digit
        self.pos_x = self.base_x - (num_digits - 1) * 8
        
        return


    def Render(self, surf):
        # Render the text
        self.game.default_font.Render_Word(surf, str(self.stored_souls), (self.pos_x, self.pos_y))


        scaled_soul_image = pygame.transform.scale(self.game.assets[keys.souls][self.animation], (16, 16))
        surf.blit(scaled_soul_image, (self.base_x + 30, self.pos_y))