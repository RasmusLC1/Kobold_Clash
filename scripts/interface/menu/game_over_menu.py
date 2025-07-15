from scripts.interface.menu.menu import Menu
from scripts.engine.keys.keys import keys


class Game_Over_Menu(Menu):
    def __init__(self, game) -> None:
        
        super().__init__(game)
        self.rect_surface.set_alpha(20) # fade in speed
        self.game_over_pos = (self.width - self.button_size_x // 2 + 20, self.button_size_y * 2.5)
        self.soul_pos = (self.width - self.button_size_x // 2 + 40, self.button_size_y * 4)
        self.gold_pos = (self.width - self.button_size_x // 2 + 40, self.button_size_y * 5)


    def Init_Buttons(self):
        self.buttons = []
        

        self.Generate_Button((self.width - self.button_size_x // 2, self.button_size_y * 6), (self.button_size_x, self.button_size_y), 'New Game', 'new_game')
        self.Generate_Button((self.width - self.button_size_x // 2, self.button_size_y * 7.5), (self.button_size_x, self.button_size_y), 'Main Menu', 'main_menu')
        self.Generate_Button((self.width - self.button_size_x // 2, self.button_size_y * 9), (self.button_size_x, self.button_size_y), 'Exit Game', 'exit_game')


    def Set_Screen_Size(self, resize_screen):
        if super().Set_Screen_Size(resize_screen):
            return
        y_factor = 2.5
        for button in self.buttons:
            button.Update_Pos((self.width - self.button_size_x // 2, self.button_size_y * y_factor))
            y_factor += 2
    
    def Render(self, surf):
        super().Render(surf)
        self.game.default_font.Render_Word(surf, "Game Over", self.game_over_pos, keys.player_damage_font)
        self.game.mixed_symbols.Render_Mixed_Text(surf, f"{self.game.player.souls} soul", self.soul_pos)
        self.game.mixed_symbols.Render_Mixed_Text(surf, f"{self.game.inventory.item_inventory.Check_Gold_In_Inventory()} gold", self.gold_pos)