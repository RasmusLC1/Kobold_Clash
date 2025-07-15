import pygame
import math
from scripts.engine.keys.keys import keys

class UI_Interface:
    def __init__(self, game, pos_x, pos_y, max_animation):
        self.game = game
        self.animation = 0
        self.cooldown = 0
        self.max_animation = max_animation
        self.base_x = pos_x
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.stored_souls = -99999

    def Update(self):
        self.Update_Animation()
        self.move_text_based_on_soul()

    def Update_Animation(self):
        if not self.cooldown:
            if self.animation >= self.max_animation:
                self.animation = 0
            else:
                self.animation += 1
            self.cooldown = 20

        self.cooldown -= 1

    def move_text_based_on_soul(self):

        if self.stored_souls == self.game.player.souls:
            return

        self.stored_souls = self.game.player.souls
        # Get the number of digits in the soul count
        num_digits = math.floor(math.log10(self)) + 1 if self.stored_souls > 0 else 1
        
        # Calculate the new position by moving 8 pixels left per extra digit
        self.pos_x = self.base_x - (num_digits - 1) * 8
        
        return


    def Render(self, surf):

        # Render the text
        self.game.default_font.Render_Word(surf, str(self.stored_souls), (self.pos_x, self.pos_y))


        scaled_soul_image = pygame.transform.scale(self.game.assets[keys.souls][self.animation], (16, 16))
        surf.blit(scaled_soul_image, (self.pos_x + 30, self.pos_y))