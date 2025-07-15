from scripts.interface.menu.menu import Menu
from scripts.engine.keys.keys import keys

class Pause_Menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        

    def Init_Buttons(self):
        width = self.game.screen_width // self.game.render_scale // 2
        # Resume Button
        self.Generate_Button((width - self.button_size_x // 2, self.button_size_y * 2.5), (self.button_size_x, self.button_size_y), 'resume', 'run_game')
        self.Generate_Button((width - self.button_size_x // 2, self.button_size_y * 4.5), (self.button_size_x, self.button_size_y), 'Main Menu', 'return_main_menu', True)
        self.Generate_Button((width - self.button_size_x // 2, self.button_size_y * 6.5), (self.button_size_x, self.button_size_y), 'Desktop', 'exit_game_save')


    def Check_Keyboard_Input(self):
         if self.game.keyboard_handler.escape_pressed:
            self.game.keyboard_handler.Set_Escape_Key(False)
            self.game.state_machine.Set_State('run_game')


    def Set_Screen_Size(self, resize_screen):
        if super().Set_Screen_Size(resize_screen):
            return
        y_factor = 2.5
        for button in self.buttons:
            button.Update_Pos((self.width - self.button_size_x // 2, self.button_size_y * y_factor))
            y_factor += 2
        