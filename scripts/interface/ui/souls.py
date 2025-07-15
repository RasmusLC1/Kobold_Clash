import pygame
import math
from scripts.engine.keys.keys import keys

class Souls:
    def __init__(self, game):
        self.game = game
        self.animation = 0
        self.cooldown = 0
        self.max_animation = 3
        self.pos_x = self.game.screen_width // self.game.render_scale - 50
        self.pos_y = 40

    def Update(self):
        self.Update_Animation()

    def Update_Animation(self):
        if not self.cooldown:
            if self.animation >= self.max_animation:
                self.animation = 0
            else:
                self.animation += 1
            self.cooldown = 20

        self.cooldown -= 1

    def move_text_based_on_soul(self, soul_count, base_position_x):
        # Get the number of digits in the soul count
        num_digits = math.floor(math.log10(soul_count)) + 1 if soul_count > 0 else 1
        
        # Calculate the new position by moving 8 pixels left per extra digit
        new_position_x = base_position_x - (num_digits - 1) * 8
        
        return new_position_x


    def Render(self, surf):
        new_x = self.move_text_based_on_soul(self.game.player.souls, self.pos_x)

        # Render the text
        self.game.default_font.Render_Word(surf, str(self.game.player.souls), (new_x, self.pos_y))


        scaled_soul_image = pygame.transform.scale(self.game.assets[keys.souls][self.animation], (16, 16))
        surf.blit(scaled_soul_image, (self.pos_x + 30, self.pos_y))