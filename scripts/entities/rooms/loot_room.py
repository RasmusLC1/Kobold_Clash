import random
from scripts.engine.keys.keys import keys


class Loot_Room():
    def Spawn_Loot_Room(self, game):
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
            decorations.update(self.Spawn_Loot_Room_Decoration(game.tilemap, decorations, library))
        return decorations
    
    def Spawn_Loot_Room_Decoration(self, tilemap, decorations, library):
        start_y = library['start_y']
        size_y = library['size_y']
        start_x = library['start_x']
        size_x = library['size_x']
        door_location = library['door_location']

        drop_table = {
            keys.weapon_rack : 0.5,
            keys.chest : 0.7,
            keys.vase : 1,
            keys.plinth : 0.1,
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

                
                if tile.contains_decoration:
                    continue

                decoration = random.choices(
                    population=list(drop_table.keys()),
                    weights=list(drop_table.values()),
                    k=1
                )[0]

                if not decoration:
                    continue

                decorations[decoration].append(tile.pos)

        return decorations
                