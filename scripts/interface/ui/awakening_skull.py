from scripts.engine.keys.keys import keys
from scripts.interface.ui.ui import UI
import pygame

class Awakening_Skull(UI):
    def __init__(self, game):
        pos_x = 100
        pos_y = game.screen_height / game.render_scale - 40
        animation_max = 0
        animation_cooldown_max = 30
        super().__init__(game, pos_x, pos_y, animation_max, animation_cooldown_max)
        self.size = (32, 32)
        self.awakening_level = 0

        # Use dictionary for easy lookup
        self.awakening_symbols = {
            0: None,
            1: self.game.assets[keys.awakening_skull_1],
            2: self.game.assets[keys.awakening_skull_2],
            3: self.game.assets[keys.awakening_skull_3],
            4: self.game.assets[keys.awakening_skull_4],
            5: self.game.assets[keys.awakening_skull_5],
        }

        self.Set_Awakening(0)
        self.display_text = False

    def Update(self):
        self.Check_Mouse_Collision()
    
    def Check_Mouse_Collision(self):
        if self.awakening_level == 0:
            return
        if self.rect().colliderect(self.game.mouse.rect_pos(self.game.render_scroll)):
            self.display_text = True
        else:
            self.display_text = False

    def Update_Animation(self):
        pass
    
    def Set_Awakening(self, awakening_level):
        self.current_awakening_symbol = self.awakening_symbols.get(awakening_level)
        self.awakening_level = awakening_level


    def Render(self, surf):
        if not self.current_awakening_symbol:
            return
        if self.display_text:
            self.game.default_font.Render_Word(surf, str("AWAKENING LEVEL: " + str(self.awakening_level)), (self.pos_x, self.pos_y - 20), keys.font_small)

        surf.blit(self.current_awakening_symbol[self.animation], (self.pos_x, self.pos_y))

    def rect(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.size[0], self.size[1])
