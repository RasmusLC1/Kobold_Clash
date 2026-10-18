from .decoration_config.shared_decoration_config import SHARED_DECRATION_CONFIG
from .decoration_config.ancient_tomb_config import ANCIENT_TOMB_CONFIG
from .decoration_config.crystal_cavern_config import CRYSTAL_CAVERN_CONFIG

from .select_floor_tiles import Select_Floor_Tiles
from scripts.engine.keys.keys import keys
import random

DUNGEON_MAP = {
            keys.ancient_tomb : ANCIENT_TOMB_CONFIG,
            keys.crystal_caverns : CRYSTAL_CAVERN_CONFIG,
        }

# Called when the dungeon is loaded
class Decoration_Initialiser():
    def __init__(self, game):
        self.game = game
        self.floor_tiles_finder = Select_Floor_Tiles(game)


    def Initialise_Dungeon(self):
        decoration_config = self._Get_Decoration_Config()
        if not decoration_config:
            print("NO DECORATIONS FOUND")
            return

        return self.Get_Decorations_To_Spawn(decoration_config)

    def Get_Decorations_To_Spawn(self, decoration_config):
        decorations_to_spawn = {}
        for decoration_type, decoration_values in decoration_config:
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
                return None

            # extend, not assign: the same type can appear in more than one config
            decorations_to_spawn.setdefault(decoration_type, []).extend(tiles)

        return decorations_to_spawn

            

    def _Get_Amount_From_Range(self, amount_tuple):
        return random.randint(amount_tuple[0], amount_tuple[1])


    def _Check_If_Large(self, size):
        return size > 32

    
    def _Get_Decoration_Config(self):
        dungeon_type = self.game.dungeon_type

        dungeon_map = {
            keys.ancient_tomb : ANCIENT_TOMB_CONFIG,
            keys.crystal_caverns : CRYSTAL_CAVERN_CONFIG,
        }

        dungeon_config = dungeon_map.get(dungeon_type)
        if dungeon_config is None:
            print("DUNGEON TYPE DOES NOT EXIST", dungeon_type, dungeon_map.keys())
            return None

        # New list every call: never mutate the shared module-level config
        return list(SHARED_DECRATION_CONFIG) + list(dungeon_config)