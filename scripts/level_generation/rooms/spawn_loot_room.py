from scripts.level_generation.room_generation.rectangle_room import Rectangle_Room
from scripts.level_generation.loot.loot_spawner import Loot_Spawner
from scripts.engine.keys.keys import keys
import math
import random

tile_size = 32
class Spawn_Loot_Room():

    @staticmethod
    def Spawn_Loot_Room(map, size_x, size_y, level, player_spawn, A_Star_Search, offgrid_tiles):

        success = 0
        fail = 0

        rooms = random.randint(10, 15)

        while success <= rooms:
            room_size_x = random.randint(4, 6)
            room_size_y = random.randint(4, 6)
            start_x = random.randint(room_size_x + 4, size_x - room_size_x)
            start_y = random.randint(room_size_y + 4, size_y - room_size_y)

            # Ensure that the room is far enough away from the player
            distance = math.sqrt((player_spawn[0] - start_x) ** 2 + (player_spawn[1] - start_y) ** 2)
            if distance < 20:
                continue

            
            
            if not Rectangle_Room.Room_Structure_Rectangle(map, start_x, start_y, room_size_x, room_size_y, A_Star_Search):
                fail += 1
                if fail >= 10 + level:
                    return False
                continue


            Spawn_Loot_Room.Spawn_Loot_In_Loot_Room(start_x, start_y, room_size_x, room_size_y, offgrid_tiles)
            success += 1
        
        
        return True
    
    @staticmethod
    def Spawn_Loot_In_Loot_Room(start_x, start_y, size_x, size_y, offgrid_tiles):
        loot_count = 0
        for y in range(start_y + 1, start_y + size_y - 1):
            for x in range(start_x + 1, start_x + size_x -1):
                spawn_loot = random.randint(0, 3 + loot_count)
                if spawn_loot == 0:
                    loot_count += 1
                    offgrid_tiles.append({keys.type: keys.chest, keys.variant: 0, keys.pos: (x * tile_size, y * tile_size)})
                elif spawn_loot == 1:
                    loot_count += 1
                    offgrid_tiles.append({"type": keys.gold, "variant": 0, "pos": [x * tile_size, y * tile_size]})

        
        # Spawn a chest in case nothing else spawns as a backup
        if not loot_count:
            offgrid_tiles.append({keys.type: keys.chest, keys.variant: 0, keys.pos: (start_x + size_x // 2 * tile_size, start_y + size_y // 2 * tile_size)})

