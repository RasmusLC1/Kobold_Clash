from .validate_floor_tiles import Check_Floor_Tile
import random


MAX_FAILURE = 50
ATTEMPTS_PER_DEOCRATION = 3

class Select_Floor_Tiles():
    def __init__(self, game):
        self.game = game
        self.floor_tile_validator = Check_Floor_Tile(game)
        self._Find_Floor_Tiles()

    def _Find_Floor_Tiles(self):
        tiles = list(self.game.tilemap.Get_Floor_Tiles().values())
        self._Filter_Out_Invalid_Tiles(tiles)

    def _Filter_Out_Invalid_Tiles(self, tiles):
        self.floor_tiles = list()
        for tile in tiles:
            if (tile.physics
                or tile.room
                or tile.trap):
                continue
            
            self.floor_tiles.append(tile)


    def _Calculate_Max_Failure(self, amount):
        return min(amount * ATTEMPTS_PER_DEOCRATION, MAX_FAILURE)

    def Select_Floor_Tiles(self, amount,
                           check_for_path_to_player = False, is_large = False):
        
        attempts = self._Calculate_Max_Failure(amount)
        tiles_found = 0
        valid_tiles = []
        
        for i in range(attempts):
            if not self.floor_tiles:  # pool ran out
                break

            # Pop instead of choice: the tile leaves the pool as soon as it is
            # picked, so it can never be drawn twice
            tile = self.floor_tiles.pop(random.randrange(len(self.floor_tiles)))

            if not self.floor_tile_validator.Verify_Tile(tile,
                                                         check_for_path_to_player,
                                                         is_large):
                continue

            tiles_found += 1
            valid_tiles.append(tile)
            tile.Set_Contains_Decoration(True) # Flag the tile as having decoration

            if tiles_found >= amount:
                break 

        return valid_tiles