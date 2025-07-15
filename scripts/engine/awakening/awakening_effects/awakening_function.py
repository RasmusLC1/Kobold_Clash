from scripts.engine.keys.keys import keys
import random

class Awakening_Function():
    def __init__(self, game):
        self.game = game 

    def Set_Awakening_Level(self, awakening_level):
        pass


    def Play_Sound(self):
        value = random.randint(0, 2)

        if value == 0:
            self.game.sound_handler.Play_Sound(keys.awakening_1, 0.3)
        elif value == 1:
            self.game.sound_handler.Play_Sound(keys.awakening_2, 0.3)
        else:
            self.game.sound_handler.Play_Sound(keys.awakening_3, 0.3)