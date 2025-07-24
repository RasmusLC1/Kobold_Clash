import random
from scripts.level_generation.dungeon_enum_keys import *
from scripts.engine.keys.keys import keys
import math
class Portal_Shrine_Spawner():

    @staticmethod
    def Spawn_Portal_Shrine(map, player_spawn, size_x, size_y, tile_size, A_Star_Search, offgrid_tiles):
        loot_amount = random.randint(1, 2)
        loot = 0 
        path = []
        count = 0
        while loot < loot_amount:

            spawner_x = random.randint(1, size_x - 2)
            spawner_y = random.randint(1, size_y - 2)
            # Ensure that the room is far enough away from the player
            distance = math.sqrt((player_spawn[0] - spawner_x) ** 2 + (player_spawn[1] - spawner_y) ** 2)
            if count > 100:
                return False
            count += 1
            if distance < 70:
                continue
            if map[spawner_x][spawner_y] != FLOOR:
                continue
            path = A_Star_Search(spawner_x, spawner_y)
            
            if path:
                offgrid_tiles.append({keys.type: keys.portal_shrine, keys.variant: 0, keys.pos: (spawner_x * tile_size, spawner_y * tile_size)})

                loot += 1

        return True