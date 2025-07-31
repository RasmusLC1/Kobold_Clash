import random
from scripts.engine.keys.keys import keys


class Loot_Room():
    def Spawn_Room(game, decorations):
        pass

    def Spawn_Room_Decoration(tilemap, decorations, room, drop_table):
        start_x, start_y = room[keys.pos]
        size_x, size_y = room[keys.size]
        door_location = room[keys.door]

        adjusted_x = start_x // 32
        adjusted_y = start_y // 32

   
        for y in range(adjusted_y + 1, adjusted_y + size_y - 1):
            # Prevent bookhelfs from spawning on same x and y axis as the door
            if y == door_location[1] and size_y > 3:
                continue
            for x in range(adjusted_x + 1, adjusted_x + size_x -1):
                if x == door_location[0] and size_x > 3: # Prevent small rooms from having no content
                    continue
                tile_key = str(int(x)) + ';' + str(int(y))
                tile = tilemap.Current_Tile(tile_key)
                
                if not tile:
                    continue

                if tile.physics:
                    continue


                tile.Set_Room(True)

                
                if tile.contains_decoration:
                    continue

                decoration = random.choices(
                    population=list(drop_table.keys()),
                    weights=list(drop_table.values()),
                    k=1
                )[0]

                if not decoration:
                    continue

                decorations[decoration].append((tile.pos[0] * 32, tile.pos[1] * 32))


        return decorations
                