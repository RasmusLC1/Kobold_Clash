import pygame
from scripts.interface.menu.button import Button
from scripts.engine.keys.keys import keys

class Menu():
    def __init__(self, game) -> None:
        self.game = game
        self.background_color = (20, 20, 20)
        self.Set_Screen_Size(False)
        self.buttons = []
        self.pos_x = 0
        self.pos_y = 0
        self.button_size_x = 200
        self.button_size_y = 40
        self.width = self.game.screen_width // self.game.render_scale // 2
        
        
        self.Init_Buttons()


    def Set_Screen_Size(self, resize_screen):
        self.size_x = self.game.screen_width // self.game.render_scale
        self.size_y = self.game.screen_height // self.game.render_scale
        self.rect_surface = pygame.Surface((self.size_x, self.size_y))
        alpha = 2
        self.rect_surface.set_alpha(alpha)
        self.rect_surface.fill(self.background_color)
        

        if resize_screen:
            self.width = self.game.screen_width // self.game.render_scale // 2
            return False
        
        return True
        




    def Init_Buttons(self):
        pass


    def Generate_Button(self, pos, size, text, menu_state, save_game = False, color = (0, 0, 0)):
        button = Button(self.game, pos, size, text, menu_state, save_game, color)
        self.buttons.append(button)



    def Update(self):
        self.Check_Keyboard_Input()
        
        for button in self.buttons:
            button.Update()

    def Render(self, surf):

        surf.blit(self.rect_surface, (self.pos_x, self.pos_y))
        for button in self.buttons:

            button.Render(surf)



    def Check_Keyboard_Input(self):
        pass

