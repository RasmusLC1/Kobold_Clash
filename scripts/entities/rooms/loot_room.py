import random
from scripts.engine.keys.keys import keys


class Loot_Room():
    def Spawn_Loot_Room(game):
        loot_rooms = game.tilemap.extract([(keys.room, keys.loot_room)])
        decorations = {}

        if keys.weapon_rack not in decorations:
            decorations[keys.weapon_rack] = []
        if keys.chest not in decorations:
            decorations[keys.chest] = []
        if keys.plinth not in decorations:
            decorations[keys.plinth] = []
        if keys.vase not in decorations:
            decorations[keys.vase] = []
        

        for library in loot_rooms:
            decorations.update(Loot_Room.Spawn_Loot_Room_Decoration(game.tilemap, decorations, library))
        return decorations
    
    def Spawn_Loot_Room_Decoration(tilemap, decorations, loot_room):
        start_x, start_y = loot_room[keys.pos]
        size_x, size_y = loot_room[keys.size]

        adjusted_x = start_x // 32
        adjusted_y = start_y // 32

        drop_table = {
            keys.weapon_rack : 0.5,
            keys.chest : 0.7,
            keys.vase : 1,
            keys.plinth : 0.1,
            None : 1
        }

        for y in range(adjusted_y + 1, adjusted_y + size_y - 1):

            for x in range(adjusted_x + 1, adjusted_x + size_x -1):
  
                tile_key = str(int(x)) + ';' + str(int(y))

                tile = tilemap.Current_Tile(tile_key)

                if not tile:
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
                