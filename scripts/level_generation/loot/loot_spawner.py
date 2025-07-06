from scripts.level_generation.dungeon_enum_keys import *
from scripts.engine.keys.keys import keys
import random

class Loot_Spawner():

    @staticmethod

    def Spawn_Loot(map, amount, item, tile_size, size_x, size_y, offgrid_tiles):
        loot = 0
        while loot <= amount:
            pos_x = random.randint(2, size_x - 3)
            pos_y = random.randint(2, size_y - 3)
            if not map[pos_x][pos_y] == FLOOR:
                continue
            offgrid_tiles.append({"type": item, "variant": 0, "pos": [pos_x * tile_size, pos_y * tile_size]})
            loot += 1
