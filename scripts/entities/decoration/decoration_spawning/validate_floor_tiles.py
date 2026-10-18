class Check_Floor_Tile():
    def __init__(self, game):
         self.game = game

    # Returns True if tile is good and False if not
    def Verify_Tile(self, floor_tile, path_find_to_player=False, is_large=False):
        # Cheap attribute checks first
        if (floor_tile.contains_decoration):
            return False

        # Then the neighbour scan, then pathfinding last since A* is the expensive one
        if not self._Check_Neighbours(floor_tile, is_large):
            return False

        return self._Check_Path_Finding_To_Player(floor_tile, path_find_to_player)


    def _Check_Path_Finding_To_Player(self, floor_tile, path_find_to_player):
        if not path_find_to_player:
            return True
        reachable = self._Get_Reachable()
        if not reachable:  # player tile is blocked, so nothing can be reached
            return True    # or False, whichever fallback you want
        return floor_tile.pos in reachable

    def _Check_Neighbours(self, floor_tile, is_large):
        # Early exit if not large always True
        if not is_large:
            return True
        
        return not self.game.tilemap.Check_If_Neighbor_Tiles_Contain_Decoration(floor_tile) 

    def _Get_Reachable(self):
        if self._reachable is None:
            ts = self.game.tilemap.tile_size
            px, py = self.game.player.pos
            start = (int(px // ts), int(py // ts))
            self._reachable = self.game.pathfinding.Flood_Reachable(start)
        return self._reachable