from scripts.level_generation.room_generation.rectangle_room import Rectangle_Room
from scripts.level_generation.loot.loot_spawner import Loot_Spawner
from scripts.engine.keys.keys import keys
import math
import random

tile_size = 32


class Spawn_Loot_Room():

    @staticmethod
    # Checks for overlaps, by having an array of positions and checks if there are collisions between them
    def overlaps(x1, y1, w1, h1, x2, y2, w2, h2):
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)

    @staticmethod
    def Spawn_Loot_Room(map, size_x, size_y, level, player_spawn, A_Star_Search, offgrid_tiles):
        success = 0
        fail = 0
        rooms = random.randint(15, 25)
        existing_rooms = []

        room_types = {
            keys.library : 0.5,
            keys.treasure_room : 1,
        }

        room_sizes = {
            keys.library : (random.randint(4, 6), random.randint(4, 6)),
            keys.treasure_room : (random.randint(3, 5), random.randint(3, 5)),
        }

        while success <= rooms:
            room_type = random.choices(
                    population=list(room_types.keys()),
                    weights=list(room_types.values()),
                    k=1
                )[0]
            
            room_size_x, room_size_y = room_sizes.get(room_type)

            start_x = random.randint(room_size_x + 4, size_x - room_size_x - 1)
            start_y = random.randint(room_size_y + 4, size_y - room_size_y - 1)

            # Ensure room is far enough from the player
            distance = math.hypot(player_spawn[0] - start_x, player_spawn[1] - start_y)
            if distance < 20:
                continue

            # Check for overlaps
            overlap = False
            for room in existing_rooms:
                if Spawn_Loot_Room.overlaps(start_x, start_y, room_size_x, room_size_y, *room):
                    overlap = True
                    break
            if overlap:
                continue
            
            door_location = Rectangle_Room.Room_Structure_Rectangle(map, start_x, start_y, room_size_x, room_size_y, A_Star_Search)
            # Try to place the room
            if not door_location:
                fail += 1
                if fail >= rooms * 2:
                    return False
                continue

            # Add room data
            existing_rooms.append((start_x, start_y, room_size_x, room_size_y))
            offgrid_tiles.append({
                keys.type: keys.room,
                keys.variant: room_type,
                keys.pos: (start_x * tile_size, start_y * tile_size),
                keys.size: (room_size_x, room_size_y),
                keys.door_basic: door_location,
                "ID": success,
            })
            success += 1

        return True

