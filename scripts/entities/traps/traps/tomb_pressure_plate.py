from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import random

CLATTER_RANGE = 500
RADIUS = 20
TOMB_AMOUNT = random.randint(1, 3)
TILESIZE = 32
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]


class Tomb_Pressure_Plate(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.pressure_plate)
        self.linked_tombs = []

    def Spawn_Tombs(self):
        pos_scaled = list(self.pos[0] // TILESIZE, self.pos[1] // TILESIZE)
        tomb_spawned = 0
        fail = 0
        while tomb_spawned < TOMB_AMOUNT:
            tile_pos_x = random.randint(pos_scaled[0] - RADIUS, pos_scaled[0] + RADIUS)
            tile_pos_y = random.randint(pos_scaled[1] - RADIUS, pos_scaled[1] + RADIUS)

            if self.Check_Neighbours(tile_pos_x, tile_pos_y):
                tomb = self.game.decoration_handler.spawn_methods(keys.effigy_tomb, (tile_pos_x * TILESIZE, tile_pos_y * TILESIZE))
                if not tomb:
                    print("SPAWNING TOMB FAILED")
                    continue
                self.linked_tombs.append(tomb)
                tomb_spawned += 1
                continue

            fail += 1
            if fail > 15:
                return


    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return
        
        self.game.clatter.Generate_Clatter(self.pos, CLATTER_RANGE) # Generate clatter to alert nearby enemies

            

    def Check_Neighbours(self, x, y):
        tilemap = self.game.tilemap.tilemap

        for offset in NEIGHBOR_OFFSETS:
            nx, ny = x + offset[0], y + offset[1] # Get neigbour key
            neighbor_key = f"{nx};{ny}"

            if neighbor_key not in tilemap:
                continue

            neighbor_tile = tilemap[neighbor_key]

            if neighbor_tile.contains_decoration or neighbor_tile.physics or neighbor_tile.room:
                return False
            
        return True