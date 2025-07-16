
from scripts.game.camera_update import Camera_Update
from scripts.game.logic_update import Logic_Update
from scripts.game.renderer import Renderer
from scripts.game.game_initialiser import Game_Initialiser
from scripts.game.level_loader import Level_Loader
import pygame
import sys
from scripts.engine.keys.keys import keys


class State_Machine():
    def __init__(self, game) -> None:
        self.game = game
        self.game_state = 'init'
        self.game.game_initialiser = Game_Initialiser(self.game)
        self.game.game_initialiser.Initialise_Game()
        self.game.renderer = Renderer(self.game)
        self.game.level_loader = Level_Loader(self.game)
        self.game.camera_update = Camera_Update(self.game)
        self.game.logic_update = Logic_Update(self.game)

        self.game_states = {
            'run_game' : self.Game_Loop,
            'main_menu' : lambda: self.Main_Menu(False),
            'return_main_menu' : lambda: self.Main_Menu(True),
            'pause_menu' : self.Pause_Menu,
            'rune_shrine_menu' : self.Rune_Shrine_Menu,
            'portal_shrine_menu' : self.Portal_Shrine_Menu,
            'exit_game' : lambda: self.Exit_Game(False),
            'exit_game_save' : lambda: self.Exit_Game(True),
            'load_game' : self.Game_Load,
            'new_game' : self.New_Game,
            'init' : self.Initialise_Game,
            'new_level' : self.New_Level,
            'game_over' : self.Game_Over_Menu,
        }


    # def Game_State(self):
    #     game_state = self.game_states.get(self.game_state)
    #     game_state()

    def Game_State(self, delta_time):
        game_state = self.game_states.get(self.game_state)
        if game_state:
            if self.game_state == "run_game":
                game_state(delta_time)
            else:
                game_state()


    def Initialise_Game(self):
        self.game_state = 'main_menu'


    def Set_State(self, state):
        self.game_state = state
        

    def Game_Load(self):

        self.game.level_loader.load_level_From_Save(self.game.level)

        self.Set_State('run_game')

    
    
    def New_Game(self):
        self.game.menu_handler.Loading_Menu_Reset()
        self.game.level_loader.Load_Level_New_Map(self.game.level)

        self.Set_State('run_game')

    def New_Level(self):
        self.game.menu_handler.Loading_Menu_Reset()
        self.game.menu_handler.portal_shrine_menu.Reset()
        player_health = self.game.player.health
        player_souls = self.game.player.Get_Total_Available_Souls()
        self.game.level += 1
        self.game.level_loader.Load_Level_New_Map(self.game.level, False)
        # Reset player health and souls
        self.game.player.Set_Souls(player_souls)
        self.game.player.Set_Health(player_health)

        self.Set_State('run_game')

    def Game_Loop(self, delta_time):
        self.game.camera_update.Camera_Scroll()
        self.game.renderer.Render()
        self.game.logic_update.Update(delta_time)

    def Main_Menu(self, save_game):
        self.game.menu_handler.Select_Menu('main_menu')
        if save_game:
            self.game.save_load_manager.Save_Data_Structure()
            self.game.level_loader.Clear_Level(True)
            self.game_state = "main_menu"

        

    def Pause_Menu(self):
        self.game.menu_handler.Select_Menu('pause_menu')

    def Game_Over_Menu(self):
        self.game.menu_handler.Select_Menu('game_over_menu')
    


    def Rune_Shrine_Menu(self):
        self.game.menu_handler.Select_Menu('rune_shrine_menu')

        # Reset the buy menu if exited
        if self.game_state != 'rune_shrine_menu':
            self.game.menu_handler.rune_shrine_menu.Reset_Rune_Bought()

    def Portal_Shrine_Menu(self):
        self.game.menu_handler.Select_Menu('portal_shrine_menu')

        # # Reset the buy menu if exited
        # if self.game_state != 'rune_shrine_menu':
        #     self.game.menu_handler.rune_shrine_menu.Reset_Rune_Bought()
  

    def Exit_Game(self, save_game):
        if save_game:
            self.game.save_load_manager.Save_Data_Structure()
        pygame.quit()
        sys.exit()

