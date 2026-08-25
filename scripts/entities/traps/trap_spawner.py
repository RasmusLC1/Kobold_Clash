from scripts.entities.traps.traps.shared import shared_registry as trap_registry
from scripts.entities.traps.traps.shared import load_all

from scripts.entities.traps.traps.ancient_tomb import ancient_tomb_registry as ancient_tomb_trap_registry
from scripts.entities.traps.traps.ancient_tomb import load_all

from scripts.entities.traps.traps.crystal_caverns import crystal_cavern_registry as crystal_cavern_trap_registry
from scripts.entities.traps.traps.crystal_caverns import load_all

from scripts.engine.keys.keys import keys
import random


TILESIZE = 32
TRAP_DENSITY = 30  # Lower = more traps

DUNGEON_TRAP_REGISTRIES = {
    keys.ancient_crypt: ancient_tomb_trap_registry,
    keys.crystal_caverns: crystal_cavern_trap_registry,
}


class Trap_Spawner():
    def __init__(self, game, trap_density=(8 * 8)):
        self.game = game
        self.trap_density = trap_density  # squared distance
        self.traps = []
        self.floor_tiles = {}
        self.traps_to_spawn = {}
        self.trap_classes = None
        self.TRAP_TABLE = None
        self.Get_Dungeon_Type()

    def Get_Dungeon_Type(self):
        dungeon_specific = DUNGEON_TRAP_REGISTRIES.get(self.game.dungeon_type)
        if dungeon_specific is None:
            raise ValueError(f"No trap registry found for dungeon type: {self.game.dungeon_type}")

        self.trap_classes = {**trap_registry.TRAP_REGISTRY, **dungeon_specific.TRAP_REGISTRY}
        self.TRAP_TABLE = {**trap_registry.TRAP_TABLE, **dungeon_specific.TRAP_TABLE}

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
        env_types = [
            keys.lava_env,
            keys.shallow_water_env, keys.medium_water_env, keys.deep_water_env,
            keys.shallow_ice_env, keys.medium_ice_env, keys.deep_ice_env,
        ]
        for env_type in env_types:
            for trap in self.game.tilemap.extract([(env_type, 0)], True):
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

                # Check distance to all previously placed traps
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