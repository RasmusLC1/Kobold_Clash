import math

class Tile_Navigation:
    __slots__ = ['tile', 'distance_to_player', 'last_distance_update_timestamp']

    def __init__(self, tile):
        self.tile = tile
        self.distance_to_player = 999.0
        self.last_distance_update_timestamp = -1.0

    def Get_Distance(self):
        if self.tile.physics or self.tile.touching_wall or self.tile.trap:
            return None
        
        if self.tile.game.total_time - self.last_distance_update_timestamp > 0.5:
            player_pos = self.tile.game.player.pos
            dx = self.tile.scaled_pos[0] - player_pos[0]
            dy = self.tile.scaled_pos[1] - player_pos[1]
            self.distance_to_player = math.sqrt(dx**2 + dy**2)
            self.last_distance_update_timestamp = self.tile.game.total_time

        return self.distance_to_player