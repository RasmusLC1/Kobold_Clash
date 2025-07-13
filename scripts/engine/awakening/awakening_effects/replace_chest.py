from scripts.engine.keys.keys import keys
import random

class Replace_Chests():
    def __init__(self, game):
        self.game = game

    def Replace_Chest(self):

        chest = self.game.decoration_handler.Get_Random_Decoration_Of_Type(keys.chest)

        chest_pos = chest.pos.copy()

        chest.Delete()

        self.game.decoration_handler.Spawn_Mimic_Chest(chest_pos)

        value = random.randint(0, 1)

        if value == 0:
            self.game.sound_handler.Play_Sound(keys.awakening_1, 0.3)
        else:
            self.game.sound_handler.Play_Sound(keys.awakening_2, 0.3)
