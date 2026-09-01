import pygame
import random
from scripts.entities.decoration.shared.loot_container.loot_container import Loot_Container
from scripts.entities.decoration.shared.shared_registry import Register_Decoration
from scripts.engine.keys.keys import keys



@Register_Decoration(keys.vase)
class Vase(Loot_Container):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.vase, pos, (32, 32), True, 5, 'vase_shatter', 600)
        self.animation = random.randint(0, 4)
        self.Set_Sprite()

    def Open(self):
        if not super().Open():
            return False
        
        self.game.decoration_handler.Remove_Decoration(self)

    def Get_Loot_Types(self):

        self.loot_weights = {keys.valuable : 0.8,
                             keys.key : 0.3,
                             keys.revive : 0.02,
                             keys.nothing : 1}


