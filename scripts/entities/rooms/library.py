import random
from scripts.engine.keys.keys import keys


class Library():
    def Spawn_Library(game):
        libraries = game.tilemap.extract([(keys.room, keys.library)])
        decorations = {}
        if keys.bookshelf not in decorations:
            decorations[keys.bookshelf] = []
        if keys.potion_table not in decorations:
            decorations[keys.potion_table] = []

        for library in libraries:
            decorations.update(Library.Spawn_Library_Decoration(game.tilemap, decorations, library))
        return decorations
    
    def Spawn_Library_Decoration(tilemap, decorations, library):
        start_x, start_y = library[keys.pos]
        size_x, size_y = library[keys.size]
        door_location = library[keys.door]

        adjusted_x = start_x // 32
        adjusted_y = start_y // 32

        drop_table = {
            keys.potion_table : 0.5,
            keys.bookshelf : 1,
            None : 3
        }

        for y in range(adjusted_y + 1, adjusted_y + size_y - 1):
            # Prevent bookhelfs from spawning on same x and y axis as the door
            if y == door_location[1]:
                continue
            for x in range(adjusted_x + 1, adjusted_x + size_x -1):
                if x == door_location[0]:
                    continue
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

                if decoration == keys.potion_table:
                    drop_table[decoration] /= 10

                decorations[decoration].append((tile.pos[0] * 32, tile.pos[1] * 32))


        return decorations
                