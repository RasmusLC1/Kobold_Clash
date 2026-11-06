from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from .ancient_tomb_registry import register_trap

import random

RADIUS = 10
TOMB_AMOUNT = random.randint(1, 3)
TILESIZE = 32
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]


@register_trap(keys.tomb_pressure_plate, 0.5)
class Tomb_Pressure_Plate(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.pressure_plate)
        self.linked_tombs = []
        self.Spawn_Tombs()
        self.activated = False

    
    def Save_Data(self):
        super().Save_Data()
        self.saved_data['activated'] = self.activated

    
    def Load_Data(self, data):
        super().Load_Data(data)
        self.activated = data['activated']

    def Spawn_Tombs(self):
        pos_scaled = [int(self.pos[0] // TILESIZE), int(self.pos[1] // TILESIZE)]
        tomb_spawned = 0
        fail = 0
        while tomb_spawned < TOMB_AMOUNT:
            tile_pos_x = random.randint(pos_scaled[0] - RADIUS, pos_scaled[0] + RADIUS)
            tile_pos_y = random.randint(pos_scaled[1] - RADIUS, pos_scaled[1] + RADIUS)

            if self.Check_Neighbours(tile_pos_x, tile_pos_y):
                tomb = self.game.decoration_handler.Decoration_Spawner(keys.effigy_tomb, (tile_pos_x * TILESIZE, tile_pos_y * TILESIZE))
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
        if self.activated or entity.type != keys.player:
            return
        
        for tomb in self.linked_tombs:
            tomb.Set_Loot_To_Always_Spawn_Enemy()
            tomb.Open()

        self.activated = True
        self.game.sound_handler.Play_Sound(keys.pressure_plate, 0.7)
        self.linked_tombs.clear()


            

    def Check_Neighbours(self, x, y):
        tilemap = self.game.tilemap.tilemap

        for offset in NEIGHBOR_OFFSETS:
            nx, ny = x + offset[0], y + offset[1] # Get neigbour key
            neighbor_key = (nx, ny)

            if neighbor_key not in tilemap:
                return False

            neighbor_tile = tilemap[neighbor_key]

            if neighbor_tile.contains_decoration or neighbor_tile.physics or neighbor_tile.room:
                return False
            
        return True