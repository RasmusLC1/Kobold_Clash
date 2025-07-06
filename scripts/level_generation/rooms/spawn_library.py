from scripts.level_generation.room_generation.rectangle_room import Rectangle_Room
from scripts.level_generation.loot.loot_spawner import Loot_Spawner
from scripts.engine.keys.keys import keys
import math
import random

tile_size = 32
class Spawn_Library():

    @staticmethod
    def Spawn_Library(map, size_x, size_y, level, player_spawn, A_Star_Search, offgrid_tiles):

        success = 0
        fail = 0

        rooms = random.randint(10, 20)

        while success <= rooms:
            room_size_x = random.randint(6, 8)
            room_size_y = random.randint(6, 8)
            start_x = random.randint(room_size_x + 4, size_x - room_size_x)
            start_y = random.randint(room_size_y + 4, size_y - room_size_y)

            # Ensure that the room is far enough away from the player
            distance = math.sqrt((player_spawn[0] - start_x) ** 2 + (player_spawn[1] - start_y) ** 2)
            if distance < 20:
                continue
            
            door_location = Rectangle_Room.Room_Structure_Rectangle(map, start_x, start_y, room_size_x, room_size_y, A_Star_Search)
            if not door_location:
                fail += 1
                if fail >= 10 + level:
                    return False
                continue


            Spawn_Library.Spawn_Loot_In_Loot_Room(start_x, start_y, room_size_x, room_size_y, offgrid_tiles, door_location)
            success += 1
        
        
        return True
    
    @staticmethod
    def Spawn_Loot_In_Loot_Room(start_x, start_y, size_x, size_y, offgrid_tiles, door_location):
        loot_count = 0
        table_spawned = False
        for y in range(start_y + 1, start_y + size_y - 1):
            # Prevent bookhelfs from spawning on same x and y axis as the door
            if y == door_location[1]:
                continue
            for x in range(start_x + 1, start_x + size_x -1):
                if x == door_location[0]:
                    continue
                spawn_loot = random.randint(0, loot_count)
                if spawn_loot == 0: # guranteed to spawn at least one bookshelf since count starts at 0
                    loot_count += 1
                    offgrid_tiles.append({keys.type: keys.bookshelf, keys.variant: 0, keys.pos: (x * tile_size, y * tile_size)})
                    continue
                
                # Spawn a single table
                if not table_spawned:
                    table_spawned = True
                    loot_count += 1
                    offgrid_tiles.append({keys.type: keys.potion_table, keys.variant: 0, keys.pos: (x * tile_size, y * tile_size)})
                    continue