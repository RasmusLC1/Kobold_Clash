from scripts.engine.keys.keys import keys

import random

class Spawn_Elite():
    def __init__(self, game):
        self.game = game

    def Spawn_Enemy(self):

        enemies = [
            keys.wight_king,
            keys.vampire,
        ]
        enemy_type = random.choice(enemies)
        if not enemy_type:
            return
        self.game.sound_handler.Play_Sound(keys.enemy_spawning, 0.3)
        tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
        pos = list((tile.pos[0] * 32, tile.pos[1] * 32))
        self.game.enemy_handler.Enemy_Spawner(pos, enemy_type)