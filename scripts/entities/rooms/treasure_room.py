import random
from scripts.engine.keys.keys import keys


class Treasure_Room():
    def Spawn_Treasure_Room(game, decorations):
        loot_rooms = game.tilemap.extract([(keys.room, keys.treasure_room)])
        if keys.weapon_rack not in decorations:
            decorations[keys.weapon_rack] = []
        if keys.chest not in decorations:
            decorations[keys.chest] = []
        if keys.plinth not in decorations:
            decorations[keys.plinth] = []
        if keys.vase not in decorations:
            decorations[keys.vase] = []
        
        print("LOOT ROOM LENGTH", len(loot_rooms))
        for loot_room in loot_rooms:
            decorations.update(Treasure_Room.Spawn_Loot_Room_Decoration(game.tilemap, decorations, loot_room))
        return decorations
    
    def Spawn_Loot_Room_Decoration(tilemap, decorations, loot_room):
        loot_count = 0
        start_x, start_y = loot_room[keys.pos]
        size_x, size_y = loot_room[keys.size]

        adjusted_x = start_x // 32
        adjusted_y = start_y // 32

        drop_table = {
            keys.weapon_rack : 0.5,
            keys.chest : 0.7,
            keys.vase : 1,
            None : 2
        }

        for y in range(adjusted_y + 1, adjusted_y + size_y - 1):

            for x in range(adjusted_x + 1, adjusted_x + size_x -1):
  
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
                
                loot_count += 1
                decorations[decoration].append((tile.pos[0] * 32, tile.pos[1] * 32))
        print(loot_count)
        return decorations
                