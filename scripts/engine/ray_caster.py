import math
import pygame
from scripts.engine.keys.keys import keys

class Ray_Caster():
    def __init__(self, game):
        self.tiles = []
        
        self.nearby_cooldown = 0
        self.inactive_distance = 800
        
        self.game = game
        self.default_activity = 700

        self.disable_distance_debugger = False

        # Basic raycasting attributes
        self.num_lines = 80 # Define the number of lines and the spread angle (in degrees)
        self.spread_angle = 360  # Total spread of the fan (in degrees)
        self.angle_increment = self.spread_angle / (self.num_lines - 1) # Calculate the angle increment between each line
        self.angles = []

    def Update(self):
        if self.disable_distance_debugger:
            return
        
        self.Check_Tile_Active()

        self.Update_Entities()


    def Update_Entities(self):
        for tile in self.tiles:
            tile.Set_Entity_Active()

    # Handle tile activity degradation
    def Check_Tile_Active(self):
        for tile in self.tiles:
            if tile.active:
                tile.active -= 1
            # Find distance from player and if it's greater than 300, delete it
            distance = math.sqrt((self.game.player.pos[0] - tile.pos[0] * self.game.tilemap.tile_size) ** 2 + (self.game.player.pos[1] - tile.pos[1] * self.game.tilemap.tile_size) ** 2)
            
            
            if abs(distance) > self.inactive_distance:
                tile.active = 0
                self.tiles.remove(tile)
    
    def Remove_Tile(self, tile):
        if tile not in self.tiles:
            return
        tile.active = 0
        self.tiles.remove(tile)

    def Check_Tile(self, tile):
        tile = self.game.tilemap.Current_Tile(tile)
        if tile:
            if not tile.active:
                tile.Set_Active(self.default_activity)
                self.tiles.append(tile)
            else:
                tile.Set_Active(self.default_activity)
            if not tile.type:
                print(tile)
                return False
            
            if not tile.translucent:
                return False
            
            
        return True

    def Clear_Entity_From_Tiles(self, entity_ID):
        for tile in self.tiles:
            tile.Clear_Entity(entity_ID)
    
    def Add_Tile(self, tile):
        self.tiles.append(tile)

    def Add_Tile_Around_Player(self):
        radius = 2
        (center_x, center_y) = tuple(map(int, self.game.player.tile.pos))
        for y in range(center_y - radius, center_y + radius + 1):
            for x in range(center_x - radius, center_x + radius + 1):
                tile_key = str(x) + ';' + str(y)
                if not self.Check_Tile(tile_key):
                    break


    def Ray_Caster(self):
        
        self.Add_Tile_Around_Player()

        # Calculate the starting angle
        base_angle = math.atan2(self.game.player.view_direction[1], self.game.player.view_direction[0])
        start_angle = base_angle - math.radians(self.spread_angle / 2)
        self.Check_Tile(self.game.player.tile)
        

        # Look for tiles that hit the rays
        for j in range(self.num_lines):
            angle = start_angle + j * math.radians(self.angle_increment)
            for i in range(1, round(6 * self.game.render_scale)):
                pos_x = self.game.player.pos[0] + math.cos(angle) * self.game.tilemap.tile_size * i
                pos_y = self.game.player.pos[1] + math.sin(angle) * self.game.tilemap.tile_size * i
                tile_key = str(int(pos_x) // self.game.tilemap.tile_size) + ';' + str(int(pos_y) // self.game.tilemap.tile_size)

                if not self.Check_Tile(tile_key):
                    break
    

    def rect(self, pos):
        return pygame.Rect(pos[0], pos[1], 10, 10)
    

    def Set_Disable_Distance_Debugger(self, state):
        self.disable_distance_debugger = state