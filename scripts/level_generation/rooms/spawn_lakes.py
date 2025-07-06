from scripts.level_generation.dungeon_enum_keys import *
import random
from scripts.engine.keys.keys import keys

class Spawn_Lakes():

    @staticmethod
    def Spawn_Lakes(noise_map, cellular_automata, iterations, value_1, value_2, offgrid_tiles):
        for i in range(iterations):

            density = random.randint(30, 40)
            size_x = random.randint(3, 5)
            size_y = random.randint(3, 5)
            start_x = random.randint(2, cellular_automata.size_x - size_x)
            start_y = random.randint(2, cellular_automata.size_y - size_y)
            lake_map = [[0 for _ in range(size_y)] for _ in range(size_x)]

            noise_map.Generate_Map(density, lake_map, value_1, value_2, size_x, size_y)
            cellular_automata.Refine_Level(value_1, value_2, size_x, size_y, 1, lake_map)
            i = 0
            j = 0
            for y in range(start_y, start_y + size_y):
                i = 0
                for x in range(start_x, start_x + size_x):
                    if x >= cellular_automata.size_x- 2 or y >= cellular_automata.size_y - 2:
                        break

                    cellular_automata.map[x][y] = lake_map[i][j]
                    if cellular_automata.map[x][y] == FLOOR:
                        spawn_loot = random.randint(0, 3)
                        if spawn_loot == 1:
                            offgrid_tiles.append({"type": keys.gold, "variant": 0, "pos": [x * 32, y * 32]})

                    i += 1
                j += 1

