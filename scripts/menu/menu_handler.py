from scripts.menu.pause_menu import Pause_Menu
from scripts.menu.main_menu import Main_Menu
from scripts.menu.rune_shrine_menu import Rune_Shrine_Menu
from scripts.menu.portal_shrine_menu import Portal_Shrine_Menu
from scripts.menu.loading_menu import Loading_Menu
from scripts.menu.game_over_menu import Game_Over_Menu
from scripts.engine.keys.keys import keys


class Menu_Handler():
    def __init__(self, game):
        self.game = game
        self.pause_menu = Pause_Menu(self.game)
        self.main_menu = Main_Menu(self.game)
        self.rune_shrine_menu = Rune_Shrine_Menu(self.game)
        self.portal_shrine_menu = Portal_Shrine_Menu(self.game)
        self.loading_menu = Loading_Menu(self.game)
        self.game_over_menu = Game_Over_Menu(self.game)

        self.menus = {
            'pause_menu' : self.pause_menu,
            'main_menu' : self.main_menu,
            'rune_shrine_menu': self.rune_shrine_menu,
            'portal_shrine_menu': self.portal_shrine_menu,
            'loading_menu': self.loading_menu,
            'game_over_menu': self.game_over_menu,
        }


    
    def Select_Menu(self, menu):
        menu = self.menus.get(menu)
        self.Menu_Updater(menu)

    def Menu_Updater(self, menu):
        menu.Update()
        menu.Render(self.game.display)

    def Loading_Menu_Reset(self):
        self.loading_menu.Reset()

    def Loading_Menu_Update(self, value):
        self.loading_menu.Update(value)
        self.loading_menu.Render(self.game.display)


    def Resize_Menus(self):
        self.pause_menu.Set_Screen_Size(True) 
        self.main_menu.Set_Screen_Size(True)
        self.rune_shrine_menu.Set_Screen_Size(True)
        self.loading_menu.Set_Screen_Size(True)