from scripts.engine.keys.keys import keys

import random

ASCENSION_TABLE = {
    0: {
        keys.skeleton_warrior: 1,
    },  
    1: {
        keys.skeleton_warrior: 1,
        keys.skeleton_ranger: 0.3,
        keys.spider: 0.8,
    },  
    2: {
        keys.skeleton_warrior: 0.5,
        keys.skeleton_ranger: 0.5,
        keys.spider: 0.6,
        keys.skeleton_guardian: 1,
        keys.skeleton_cleric: 0.3,
        keys.skeleton_bell_toller: 0.4,
    },
    3: {
        keys.skeleton_warrior: 0.2,
        keys.skeleton_ranger: 0.5,
        keys.spider: 0.5,
        keys.skeleton_guardian: 1.5,
        keys.skeleton_cleric: 0.3,
        keys.skeleton_bell_toller: 0.4,
        keys.skeleton_banner_bearer: 0.3,
        keys.shade: 0.5,
        keys.wraith: 0.5
    },
    4: {
        keys.skeleton_ranger: 0.7,
        keys.spider: 0.5,
        keys.skeleton_guardian: 1.3,
        keys.skeleton_cleric: 0.3,
        keys.skeleton_bell_toller: 0.4,
        keys.skeleton_banner_bearer: 0.3,
        keys.shade: 1,
        keys.wraith: 0.5,
        keys.phantom: 0.5,
        keys.ghoul: 1

    },
    5: {
        keys.skeleton_ranger: 0.7,
        keys.skeleton_guardian: 1.3,
        keys.skeleton_cleric: 0.3,
        keys.skeleton_bell_toller: 0.3,
        keys.skeleton_banner_bearer: 0.3,
        keys.shade: 1,
        keys.wraith: 0.5,
        keys.phantom: 0.5,
        keys.ghoul: 1,
        keys.skeleton_undertaker: 0.6,
        keys.skeleton_warlock: 0.3
    },
}


class Spawn_Enemies():
    def __init__(self, game):
        self.game = game
        self.enemies = {}
        self.Set_Awakening_Level(0)

    def Set_Awakening_Level(self, awakening_level):
        self.awakening_level = awakening_level

        self.enemies = ASCENSION_TABLE.get(self.awakening_level, {})

    def Spawn_Enemy(self):
        if not self.enemies:
            return
        

        enemy_amount = random.randint(1, max(1, self.awakening_level))

        for _ in range(enemy_amount):
            enemy_type = random.choices(
                        population=list(self.enemies.keys()),
                        weights=list(self.enemies.values()),
                        k=1
                    )[0]
            
            if not enemy_type:
                return

            tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
            pos = list((tile.pos[0] * 32, tile.pos[1] * 32))
            self.game.enemy_handler.Enemy_Spawner(pos, enemy_type)