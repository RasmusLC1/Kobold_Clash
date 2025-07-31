from scripts.level_generation.dungeon_enum_keys import *
from scripts.level_generation.room_generation.circle_room import Circle_Room
import random
import math
from scripts.engine.keys.keys import keys

class Spawn_Boss_Room():

    @staticmethod
    def Spawn_Boss_Room(map, tile_size, size_x, size_y, player_pos, A_Star_Search, offgrid_tiles):
        # Create backup of map
        map_copy = map.copy()
        fail = 0
        start_x = 0
        start_y = 0
        radius = 0

        while fail < 10:
            radius = random.randint(6, 8)
            start_x = random.randint(radius * 2, size_x - radius * 2)
            start_y = random.randint(radius * 2, size_y - radius * 2)
            
            distance_to_player = math.sqrt((player_pos[0] - start_x) ** 2 + (player_pos[1] - start_y) ** 2)
            fail += 1
            if distance_to_player < 50:
                continue
            path = []
            path = A_Star_Search(start_x, start_y)
            if path:
                break



        Circle_Room.Room_Structure_Circle(map, start_x, start_y, radius)

        # Ensure there's a valid path to get into the boss room
        path = A_Star_Search(start_x, start_y)
        if not path:
            map = map_copy
            Spawn_Boss_Room.Spawn_Boss_Room(map, tile_size, size_x, size_y, player_pos, A_Star_Search, offgrid_tiles)
            return

        # self.tilemap.offgrid_tiles.append({"type": 'Shrine', "variant": 0, "pos": [start_x * self.tile_size, start_y * self.tile_size]})
        offgrid_tiles.append({keys.type: keys.room, keys.variant: keys.boss_room, keys.pos: (start_x * tile_size, start_y * tile_size), keys.size : radius})

        
    @staticmethod
    def Spawn_Traps_In_Boss_Room(map, start_x, start_y, radius):
        trap_number = random.randint(1, 5)
        i = 0
        while i < trap_number:
            pos_x = random.randint(start_x - radius + 1, start_x + radius - 2)
            pos_y = random.randint(start_y - radius + 1, start_y + radius - 2)
            
            distance_from_center = math.sqrt((pos_x - start_x) ** 2 + (pos_y - start_y) ** 2)
            if distance_from_center <= 2:
                continue
            map[pos_x][pos_y] = TRAP
            i += 1