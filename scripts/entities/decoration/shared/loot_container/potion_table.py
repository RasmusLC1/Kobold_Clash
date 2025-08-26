import pygame
import random
from scripts.entities.decoration.shared.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys



class Potion_Table(Loot_Container):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.potion_table, pos, (64, 64), True, 50, 'table_break', 500)


    def Set_Loot_Types(self):

        self.loot_weights = {keys.potion : 0.8,
                             keys.recipe_scroll : 0.1,
                             }

    def Drop_Loot(self):
        loot_types = list(self.loot_weights.keys())
        for i in range(3):
            weight_values = [self.loot_weights[loot_type] for loot_type in loot_types]
            loot_type = random.choices(loot_types, weight_values, k=1)[0]
            pos = self.Get_Pos()
            if loot_type == keys.potion:
                self.Spawn_Loot(loot_type, pos)
            else:
                self.game.item_handler.loot_handler.passive_loot_handler.Loot_Spawner(pos, keys.recipe_scroll)

    def Get_Pos(self):
        rand_pos_x = self.pos[0] + random.randint(-100, 100)/5
        rand_pos_y = self.pos[1] + random.randint(-100, 100)/5
        return (rand_pos_x, rand_pos_y)