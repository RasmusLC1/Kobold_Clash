from scripts.level_generation.dungeon_enum_keys import *
import random
from scripts.engine.keys.keys import keys

class Rune_Spawner():

    @staticmethod
    def Spawn_Runes(map, level, tile_size, size_x, size_y, offgrid_tiles):
        loot_amount = random.randint(max(0, 3 - level), max(0, 5 - level))
        loot = 0 
        while loot < loot_amount:
            spawner_x = random.randint(1, size_x - 2)
            spawner_y = random.randint(1, size_y - 2)
            if map[spawner_x][spawner_y] != FLOOR:
                continue
            
            offgrid_tiles.append({keys.type: keys.plinth, keys.variant: 0, keys.pos: (spawner_x * tile_size, spawner_y * tile_size)})
            loot += 1

