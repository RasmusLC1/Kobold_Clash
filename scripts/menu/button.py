import pygame
from scripts.engine.keys.keys import keys

class Button():
    def __init__(self, game, pos, size, text, game_state, save_game = False, color = (0, 0, 0)) -> None:
        self.game = game
        self.size = size
        self.pos = pos
        self.text = text
        self.background_color = color
        self.background_color_holder = color
        self.game_state = game_state
        self.text_length = len(text)
        self.rect_surface = pygame.Surface(self.size)
        self.rect_surface.fill(self.background_color)
        self.button_speed = 4
        self.save_game = save_game

    def Update_Pos(self, pos):
        self.pos = pos
    
    def Update(self):
        self.game.mouse.Menu_Mouse_Update()
        if self.rect().colliderect(self.game.mouse.rect_pos_menu()):
            self.Handle_Button_Color()

            if self.rect().colliderect(self.game.mouse.rect_click()):
                self.game.mouse.Set_Click_Pos((-999, -999))
                self.Activate()
                return True
            return False
        
        self.Reset_Color()
        return False
    
    def Handle_Button_Color(self):
        color_0 = min(50, self.background_color[0] + self.button_speed)
        color_1 = min(50, self.background_color[1] + self.button_speed)
        color_2 = min(50, self.background_color[2] + self.button_speed)
        self.background_color = (color_0, color_1, color_2)
        self.rect_surface.fill(self.background_color)

    def Reset_Color(self):
        if self.background_color == self.background_color_holder:
            return
        
        color_0 = max(self.background_color_holder[0], self.background_color[0] - self.button_speed)
        color_1 = max(self.background_color_holder[1], self.background_color[1] - self.button_speed)
        color_2 = max(self.background_color_holder[2], self.background_color[2] - self.button_speed)
        self.background_color = (color_0, color_1, color_2)
        self.rect_surface.fill(self.background_color)

    def Activate(self):
        if self.save_game:
            self.game.save_load_manager.Save_Data_Structure()

        self.game.state_machine.Set_State(self.game_state)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def Render(self, surf):
        surf.blit(self.rect_surface, self.pos)
        self.game.default_font.Render_Word(surf, self.text, (round(self.pos[0] + self.size[0] // 2 - self.text_length * 8), self.pos[1] + self.size[1] // 2 - 8))        


