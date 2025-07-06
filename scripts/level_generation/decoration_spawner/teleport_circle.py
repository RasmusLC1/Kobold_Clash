from scripts.level_generation.dungeon_enum_keys import *
from scripts.engine.keys.keys import keys

import random
class Teleportation_Circle_Spawner():


    @staticmethod
    def Spawn_Teleport_Circle(map, size_x, size_y, tile_size, offgrid_tiles, A_Star_Search):
        loot_amount = random.randint(5, 10)
        loot = 0 
        while loot < loot_amount:
            teleport_1 = Teleportation_Circle_Spawner.Spawn_Single_Circle(map, size_x, size_y, tile_size, offgrid_tiles, A_Star_Search)
            if not teleport_1:
                continue
            teleport_2 = Teleportation_Circle_Spawner.Spawn_Single_Circle(map, size_x, size_y, tile_size, offgrid_tiles, A_Star_Search)
            if not teleport_2:
                continue
            offgrid_tiles.append(teleport_1)
            offgrid_tiles.append(teleport_2)
            loot += 1
    
    def Spawn_Single_Circle(map, size_x, size_y, tile_size, offgrid_tiles, A_Star_Search):
        path = []
        spawner_x = random.randint(1, size_x - 2)
        spawner_y = random.randint(1, size_y - 2)
        if map[spawner_x][spawner_y] != FLOOR:
            return None
        path = A_Star_Search(spawner_x, spawner_y)
        
        if path:
            key = {keys.type: keys.teleportation_circle, keys.variant: 0, keys.pos: (spawner_x * tile_size, spawner_y * tile_size)}
            return key
        
        return None