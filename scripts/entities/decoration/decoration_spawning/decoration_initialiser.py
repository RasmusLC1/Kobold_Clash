from .decoration_config.shared_decoration_config import SHARED_DECRATION_CONFIG
from .decoration_config.ancient_tomb_config import ANCIENT_TOMB_CONFIG
from .decoration_config.crystal_cavern_config import CRYSTAL_CAVERN_CONFIG

from .select_floor_tiles import Select_Floor_Tiles
from .lights_initialiser import Lights_Initialiser
from scripts.engine.keys.keys import keys
import random

DUNGEON_MAP = {
    keys.ancient_tomb : ANCIENT_TOMB_CONFIG,
    keys.crystal_caverns : CRYSTAL_CAVERN_CONFIG,
}
TILE_SIZE = 32

# Called when the dungeon is loaded
class Decoration_Initialiser():
    def __init__(self, game):
        self.game = game
        self.floor_tiles_finder = Select_Floor_Tiles(game)
        self.lights_initialiser = Lights_Initialiser(game, self.floor_tiles_finder)

    def Initialise_Dungeon(self):
        decoration_config = self._Get_Decoration_Config()
        if not decoration_config:
            print("NO DECORATIONS FOUND")
            return None

        # Lights first, so they claim their tiles before the other decorations
        lights_to_Spawn = self.lights_initialiser.Initialise_Light_Sources(decoration_config)

        print(lights_to_Spawn)

        decorations_to_spawn = self._Get_Decorations_To_Spawn(decoration_config)
        if decorations_to_spawn is None:  # a decoration type couldn't be placed
            return None

        decorations_to_spawn.update(lights_to_Spawn)
        return decorations_to_spawn
    

    def _Get_Decorations_To_Spawn(self, decoration_config):
        decorations_to_spawn = {}
        for decoration_type, decoration_values in decoration_config.items():  # .items()
            amount_tuple = decoration_values.amount
            size = decoration_values.size
            check_for_path_to_player = decoration_values.check_player_path

            amount = self._Get_Amount_From_Range(amount_tuple)
            if amount == 0:  # a range like (0, 3) can roll 0, which isn't a failure
                continue

            tiles = self.floor_tiles_finder.Select_Floor_Tiles(amount,
                                                       check_for_path_to_player,
                                                       self._Check_If_Large(size)
                                                       )
            if not tiles:
                print("NO TILES FOUND")
                return None

            decorations_to_spawn.setdefault(decoration_type, []).extend(tiles)

        return decorations_to_spawn

    def _Get_Amount_From_Range(self, amount_tuple):
        return random.randint(amount_tuple[0], amount_tuple[1])

    def _Check_If_Large(self, size):
        return max(size) > TILE_SIZE

    def _Get_Decoration_Config(self):
        dungeon_type = self.game.dungeon_type

        dungeon_config = DUNGEON_MAP.get(dungeon_type)
        if dungeon_config is None:
            print("DUNGEON TYPE DOES NOT EXIST", dungeon_type, DUNGEON_MAP.keys())
            return None

        # New dict every call: never mutate the shared module-level config.
        # On a key clash the dungeon entry replaces the shared one.
        return {**SHARED_DECRATION_CONFIG, **dungeon_config}