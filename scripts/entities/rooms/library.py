import random
from scripts.engine.keys.keys import keys


class Library():
    def Spawn_Library(self, game):
        libraries = game.tilemap.extract([(keys.room, keys.library)])
        decorations = {}

        for library in libraries:
            decorations.update(self.Spawn_Library_Decoration(game.tilemap, decorations, library))
        return decorations
    
    def Spawn_Library_Decoration(self, tilemap, decorations, library):
        start_y = library['start_y']
        size_y = library['size_y']
        start_x = library['start_x']
        size_x = library['size_x']
        door_location = library['door_location']

        drop_table = {
            keys.potion_table : 0.5,
            keys.bookshelf : 1,
            None : 3
        }

        for y in range(start_y + 1, start_y + size_y - 1):
            # Prevent bookhelfs from spawning on same x and y axis as the door
            if y == door_location[1]:
                continue
            for x in range(start_x + 1, start_x + size_x -1):
                if x == door_location[0]:
                    continue
                tile_key = (x, y)
                tile = tilemap.Current_Tile(tile_key)

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

                decorations[decoration].append(tile.pos)

        return decorations
                