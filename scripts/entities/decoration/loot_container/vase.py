import pygame
import random
from scripts.entities.decoration.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys



class Vase(Loot_Container):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.vase, pos, True, 5)
        self.animation = random.randint(0, 4)
        self.Set_Sprite()
        self.empty = True

    def Open(self):
        return

    def Set_Loot_Types(self):

        self.loot_weights = {keys.valuable : 0.8,
                             keys.key : 0.3,
                             keys.revive : 0.02,
                             keys.nothing : 1}


