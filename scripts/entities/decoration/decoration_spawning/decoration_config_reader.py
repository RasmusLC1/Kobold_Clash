from .decoration_config.shared_decoration_config import SHARED_DECRATION_CONFIG
from .decoration_config.ancient_tomb_config import ANCIENT_TOMB_CONFIG
from .decoration_config.crystal_cavern_config import CRYSTAL_CAVERN_CONFIG

from .select_floor_tiles import Select_Floor_Tiles
from scripts.engine.keys.keys import keys
import random

# Called when the dungeon is loaded
class Decoration_Initialiser():
    def __init__(self, game):
        self.game = game
        self.floor_tiles_finder = Select_Floor_Tiles(game)



    def Initialise_Dungeon(self):
        decorations_to_spawn = self.Get_Decorations_To_Spawn()
        if not decorations_to_spawn:
            print("NO DECORATIONS FOUND")
            return

    def Iterate_Over_Decorations(self, decorations_to_spawn):
        for decoration_type, decoration_values in decorations_to_spawn:
            amount_tuple = decoration_values.amount
            size = decoration_values.size
            check_for_path_to_player = decoration_values.check_player_path
            tiles = self.floor_tiles_finder.Select_Floor_Tiles(self.Get_Amount_From_Range(amount_tuple),
                                                       check_for_path_to_player,
                                                       self.Check_If_Large(size)
                                                       )
            if not tiles:
                return False

            self.Spawn_Decoration(decoration_type, tiles)

        return True
            





    def Get_Amount_From_Range(self, amount_tuple):
        return random.randint(amount_tuple[0], amount_tuple[1])


    def Check_If_Large(self, size):
        return size > 32

    def Get_Decorations_To_Spawn(self):
        dungeon_type = self.game.dungeon_type
        deocrations_to_spawn = SHARED_DECRATION_CONFIG

        dungeon_map = {
            keys.ancient_tomb : ANCIENT_TOMB_CONFIG,
            keys.crystal_caverns : CRYSTAL_CAVERN_CONFIG,
        }

        
        try:
            deocrations_to_spawn.extend(dungeon_map.get(dungeon_type))
        except Exception as e:
            print("DUNGEON TYPE DOES NOT EXIST", dungeon_type, dungeon_map.keys())
            return None

        return deocrations_to_spawn