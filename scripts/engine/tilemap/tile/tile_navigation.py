import math

class Tile_Navigation:
    __slots__ = ['tile', 'distance_to_player', 'last_distance_update_timestamp', 'last_target_pos']

    def __init__(self, tile):
        self.tile = tile
        self.distance_to_player = 999.0
        self.last_distance_update_timestamp = -1.0
        self.last_target_pos = None

    def Calculate_Distance_To_Target(self, pos):
        dx = self.tile.scaled_pos[0] - pos[0]
        dy = self.tile.scaled_pos[1] - pos[1]

        self.distance_to_player = math.sqrt(dx**2 + dy**2)
        self.last_distance_update_timestamp = self.tile.game.total_time
        self.last_target_pos = pos
        return self.distance_to_player

    def Get_Distance_To_Target(self, pos):
        # Check if half a second have passed or the target has changed
        stale = self.tile.game.total_time - self.last_distance_update_timestamp > 0.5
        moved = self.last_target_pos != pos

        if stale or moved:
            self.Calculate_Distance_To_Target(pos)

        return self.distance_to_player