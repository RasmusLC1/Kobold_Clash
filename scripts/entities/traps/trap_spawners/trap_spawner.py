from scripts.entities.traps.traps.shared.spike import Spike
from scripts.entities.traps.traps.shared.rubble import Rubble
from scripts.entities.traps.traps.shared.spike_poisoned import Spike_Poisoned
from scripts.entities.traps.traps.shared.spike_pit import Spike_Pit
from scripts.entities.traps.traps.shared.fire_trap import Fire_Trap
from scripts.entities.traps.environment.lava import Lava
from scripts.entities.traps.environment.water import Water
from scripts.entities.traps.environment.ice import Ice
from scripts.entities.traps.traps.shared.spider_web import Spider_Web
from scripts.entities.traps.traps.ancient_tomb.arrow_trap import Arrow_Trap
from scripts.engine.keys.keys import keys
import random




TILESIZE = 32
TRAP_DENSITY = 30 # Lower = more traps

class Trap_Spawner():

    TRAP_TABLE = { # Expand with new traps as needed
        keys.pit_trap : 0.4,
        keys.spike_poison_trap : 0.4,
        keys.spike_trap : 0.6,
        keys.rubble : 2,
        keys.arrow_trap : 0.3,
    }

    def __init__(self, game, extra_traps=None, extra_trap_classes=None, trap_density = (8 * 8)):
        self.game = game
        self.trap_density = trap_density # squared distance
        self.traps = []
        self.floor_tiles = {}
        self.traps_to_spawn = {}
        self.trap_classes = {
            keys.spike_trap: Spike,
            keys.spike_poison_trap: Spike_Poisoned,
            keys.pit_trap: Spike_Pit,
            keys.rubble: Rubble,
            keys.arrow_trap: Arrow_Trap,
            keys.lava_env: Lava,
            keys.fire_trap: Fire_Trap,
            keys.spider_web: Spider_Web,
            keys.shallow_ice_env: Ice,
            keys.medium_ice_env: Ice,
            keys.deep_ice_env: Ice,
            keys.shallow_water_env: Water,
            keys.medium_water_env: Water,
            keys.deep_water_env: Water,
        }
        self.TRAP_TABLE = {**self.TRAP_TABLE, **(extra_traps or {})}
        self.trap_classes = {**self.trap_classes, **(extra_trap_classes or {})}


    def Spawn_Traps(self, pos, trap_type, data=None):
        cls = self.trap_classes.get(trap_type)
        if cls is None:
            print("FAILED TO FIND TRAPTYPE", trap_type)
            return False

        if 'ice' in trap_type or 'water' in trap_type:
            trap = cls(self.game, pos, trap_type) 
        else:
            trap = cls(self.game, pos)

        if data:
            trap.Load_Data(data)

        self.traps.append(trap)
        return True
    
    def Initialise(self):
        self.traps.clear()
        self.Initialise_Traps()
        for trap_type, trap_positions in self.traps_to_spawn.items():
            for trap_pos in trap_positions:
                self.Spawn_Traps(trap_pos, trap_type)
        
        self.Spawn_Trap_Tiles()
        return self.traps

    def Spawn_Trap_Tiles(self):
        for trap in self.game.tilemap.extract([(keys.lava_env, 0)].copy(), True):
            self.Spawn_Traps(trap.pos, trap.type)

        for trap in self.game.tilemap.extract([(keys.shallow_water_env, 0)].copy(), True):
            self.Spawn_Traps(trap.pos, trap.type)


        for trap in self.game.tilemap.extract([(keys.medium_water_env, 0)].copy(), True):
            self.Spawn_Traps(trap.pos, trap.type)

        for trap in self.game.tilemap.extract([(keys.deep_water_env, 0)].copy(), True):
            self.Spawn_Traps(trap.pos, trap.type)


        for trap in self.game.tilemap.extract([(keys.shallow_ice_env, 0)].copy(), True):
            self.Spawn_Traps(trap.pos, trap.type)


        for trap in self.game.tilemap.extract([(keys.medium_ice_env, 0)].copy(), True):
            self.Spawn_Traps(trap.pos, trap.type)

        for trap in self.game.tilemap.extract([(keys.deep_ice_env, 0)].copy(), True):
            self.Spawn_Traps(trap.pos, trap.type)
    

    def Initialise_Traps(self):
        self.Get_Floor_Tiles()
        trap_tiles = []  # Keeps track of already placed trap positions (in tile coordinates)
        tilemap = self.game.tilemap
        keys_to_delete = []
        distance_between_traps = self.trap_density


        # Convert floor_tiles to a list to avoid runtime errors from modifying the dict during iteration
        for tile_key, tile in self.floor_tiles.items():
            if tile.contains_decoration:
                keys_to_delete.append(tile_key)
                continue

            i, j = tile.pos 

            # Random chance to try placing a trap at this tile
            if random.randint(0, TRAP_DENSITY) == 1:
                too_close = False

                
                # Check distance to all previously placed trapes
                for trap_pos in trap_tiles:
                    too_close = self.Check_If_Too_Close((i, j), trap_pos, distance_between_traps)
                    if too_close:
                        break

                # If no nearby trap found, place one here
                if too_close:
                    continue


                trap_tiles.append((i, j))  # Track this trap position
                trap = random.choices(
                    population=list(self.TRAP_TABLE.keys()),
                    weights=list(self.TRAP_TABLE.values()),
                    k=1
                )[0]

                if trap not in self.traps_to_spawn:
                    self.traps_to_spawn[trap] = []

                self.traps_to_spawn[trap].append((i * TILESIZE, j * TILESIZE))
                tile = tilemap.Get_Tile(tile_key)
                
                if not tile:
                    return
                tile.Set_Contains_Decoration(True)
                keys_to_delete.append(tile_key)


        # Delete keys after
        for key in keys_to_delete:
            del self.floor_tiles[key]


    def Check_If_Too_Close(self, pos_1, pos_2, distance_between_traps):
        dx = pos_1[0] - pos_2[0]
        dy = pos_1[1] - pos_2[1]
        return dx * dx + dy * dy < distance_between_traps
        

    def Get_Floor_Tiles(self):
        self.floor_tiles = self.game.tilemap.Get_Floor_Tiles()

