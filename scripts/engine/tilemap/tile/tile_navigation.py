import math

class Tile_Navigation:
    __slots__ = ['tile', 'distance_to_player', 'last_distance_update_timestamp']

    def __init__(self, tile):
        self.tile = tile
        self.distance_to_player = 999.0
        self.last_distance_update_timestamp = -1.0

    def Get_Distance(self):
        if self.tile.physics or self.tile.touching_wall:
            return None
        
        # Route through self.tile to grab the main game state clock
        if self.tile.game.total_time - self.last_distance_update_timestamp > 0.5:
            self.Calculate_Distance_To_Player()

        return self.distance_to_player

    def Calculate_Distance_To_Player(self):  
        player_pos = self.tile.game.player.pos
        # Route coordinates accurately through the parent tile's position variables
        dx = self.tile.scaled_pos[0] - player_pos[0]
        dy = self.tile.scaled_pos[1] - player_pos[1]
        
        self.distance_to_player = math.sqrt(dx**2 + dy**2)
        self.last_distance_update_timestamp = self.tile.game.total_time
        return self.distance_to_player