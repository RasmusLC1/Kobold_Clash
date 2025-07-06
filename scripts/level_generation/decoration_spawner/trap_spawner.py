from scripts.level_generation.dungeon_enum_keys import *
from scripts.engine.keys.keys import keys

import random
class Trap_Spawner(): 

    @staticmethod
    # Spawn trap if density is greater than spawn trap, goes from 0 to 100
    def Spawn_Traps(map, density, size_x, size_y):
        for y in range(1, size_y - 1):
            for x in range(1, size_x - 1):
                if map[x][y] != FLOOR:
                    continue
                spawn_trap = random.randint(0, 100)
                if spawn_trap < density:
                    map[x][y] = TRAP