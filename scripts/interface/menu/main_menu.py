from scripts.interface.menu.menu import Menu
from scripts.engine.keys.keys import keys


class Main_Menu(Menu):
    def __init__(self, game) -> None:
        
        super().__init__(game)
        self.rect_surface.set_alpha(250)

    def Init_Buttons(self):
        self.buttons = []
        # Resume Button
        self.Generate_Button((self.width - self.button_size_x // 2, self.button_size_y * 2.5), (self.button_size_x, self.button_size_y), 'New Game', 'new_game')
        self.Generate_Button((self.width - self.button_size_x // 2, self.button_size_y * 4.5), (self.button_size_x, self.button_size_y), 'Load Game', 'load_game')
        self.Generate_Button((self.width - self.button_size_x // 2, self.button_size_y * 6.5), (self.button_size_x, self.button_size_y), 'Exit Game', 'exit_game')


    def Set_Screen_Size(self, resize_screen):
        if super().Set_Screen_Size(resize_screen):
            return
        y_factor = 2.5
        for button in self.buttons:
            button.Update_Pos((self.width - self.button_size_x // 2, self.button_size_y * y_factor))
            y_factor += 2
        