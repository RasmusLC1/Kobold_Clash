from scripts.engine.ray_caster import Ray_Caster 
from scripts.entities.entity_renderer import Entity_Renderer
from scripts.engine.fonts.font import Font
from scripts.engine.fonts.mixed_symbols import Mixed_Symbols
from scripts.engine.fonts.interactable_object import Interactable_Object
from scripts.engine.fonts.noise.noise_handler import Noise_Handler
from scripts.engine.fonts.symbols import Symbols
from scripts.engine.awakening.clatter import Clatter
from scripts.entities.textbox.text_box_handler import Text_Box_handler
from scripts.engine.sound.sound_handler import Sound_Handler
from scripts.level_generation.dungeon_generator import Dungeon_Generator

from scripts.engine.tilemap.tilemap import Tilemap
from scripts.engine.assets.graphics_loader import Graphics_Loader
from scripts.engine.assets.audio_loader import Audio_Loader
from scripts.input.keyboard import Keyboard_Handler
from scripts.input.mouse import Mouse_Handler
from scripts.engine.a_star import A_Star
from scripts.interface.menu.menu_handler import Menu_Handler
from scripts.interface.ui.ui_handler import UI_Handler




import pygame

class Game_Initialiser():
    def __init__(self, game) -> None:
        self.game = game

    def Initialise_Game(self):
        self.game.render_scale = 2
        
        self.game.screen_width = 1500
        self.game.screen_height = 1000
        self.game.screen = pygame.display.set_mode((self.game.screen_width, self.game.screen_height), pygame.RESIZABLE)
        self.game.display = pygame.Surface((self.game.screen_width/self.game.render_scale, self.game.screen_height/self.game.render_scale))
        self.game.render_scroll = (0,0)
        

        self.game.assets = {}
        Graphics_Loader.Run_All(self.game)
        Audio_Loader.Run_All(self.game)
        self.game.menu_handler = Menu_Handler(self.game)

        self.initialise_Engine()


        self.game.level = 1
        self.game.scroll = [0, 0]

    def initialise_Engine(self):
        self.game.mouse = Mouse_Handler(self.game)
        self.game.ray_caster = Ray_Caster(self.game)
        self.game.a_star = A_Star(self.game)
        self.game.entities_render = Entity_Renderer(self.game)
        self.game.default_font = Font(self.game)
        self.game.symbols = Symbols(self.game)
        self.game.mixed_symbols = Mixed_Symbols(self.game, self.game.symbols, self.game.default_font)
        self.game.interactable_object = Interactable_Object(self.game)
        self.game.noise_handler = Noise_Handler(self.game)
        self.game.clatter = Clatter(self.game)
        self.game.text_box_handler = Text_Box_handler(self.game)
        self.game.sound_handler = Sound_Handler(self.game)
        self.game.keyboard_handler = Keyboard_Handler(self.game)
        
        self.game.ui_handler = UI_Handler(self.game)
        self.game.tilemap = Tilemap(self.game, tile_size=16)
        self.game.dungeon_generator = Dungeon_Generator(self.game)

        