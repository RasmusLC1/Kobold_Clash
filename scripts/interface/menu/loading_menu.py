import pygame
from scripts.interface.menu.menu import Menu
from scripts.engine.keys.keys import keys


class Loading_Menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.rect_surface.set_alpha(250)
        self.load_state = 0
        self.max_load_state = 6

        


    def Update(self, value = 0):
        self.Increment_Load_State(value)
        return super().Update()

    def Increment_Load_State(self, value):
        self.load_state = max(self.load_state, value)

    def Reset(self):
        self.load_state = 0
        return
        

    def Render(self, surf):
        

        super().Render(surf)
        loading_bar = pygame.transform.scale(self.game.assets['loading_bar'][self.load_state], (self.size_x - 20, self.size_y // 4))  
        # loading_bar = self.game.assets['loading_bar'][self.load_state]

        surf.blit(loading_bar, (10,  self.size_y - self.size_y // 4))
        self.game.screen.blit(pygame.transform.scale(self.game.display, self.game.screen.get_size()), (0,0))
        self.game.Update_Display()

        

