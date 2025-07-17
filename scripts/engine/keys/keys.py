from scripts.engine.keys.particles import Particles
from scripts.engine.keys.weapons import Weapons
from scripts.engine.keys.player import Player
from scripts.engine.keys.enemy import Enemy
from scripts.engine.keys.interface import Interface
from scripts.engine.keys.decorations import Decorations
from scripts.engine.keys.efffects import Effects
from scripts.engine.keys.items import Items
from scripts.engine.keys.game_types import Game_Types
from scripts.engine.keys.tiles import Tiles
from scripts.engine.keys.sounds import Sounds
from scripts.engine.keys.game_variables import Game_Variables

class keys(
    Particles,
    Effects,
    Weapons,
    Player,
    Enemy,
    Interface,
    Decorations,
    Items,
    Game_Types,
    Tiles,
    Sounds,
    Game_Variables
):
    pass