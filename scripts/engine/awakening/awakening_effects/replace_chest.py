from scripts.engine.keys.keys import keys
from scripts.engine.awakening.awakening_effects.awakening_function import Awakening_Function


class Replace_Chests(Awakening_Function):

    def Replace_Chest(self):

        chest = self.game.decoration_handler.Get_Random_Decoration_Of_Type(keys.chest)

        chest_pos = chest.pos.copy()

        chest.Delete()

        self.game.decoration_handler.Spawn_Mimic_Chest(chest_pos)

        self.Play_Sound()
