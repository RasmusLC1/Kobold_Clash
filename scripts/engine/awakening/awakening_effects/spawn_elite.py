from scripts.engine.keys.keys import keys
from scripts.engine.awakening.awakening_effects.awakening_function import Awakening_Function

import random

class Spawn_Elite(Awakening_Function):


    def Spawn_Enemy(self):

        enemies = [
            keys.wight_king,
            keys.vampire,
        ]
        enemy_type = random.choice(enemies)
        if not enemy_type:
            return
        
        tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
        self.game.enemy_handler.Enemy_Spawner(tile.scaled_pos, enemy_type)

        self.Play_Sound()