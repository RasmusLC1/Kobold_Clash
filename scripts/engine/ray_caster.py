import math
import pygame
from scripts.engine.keys.keys import keys

# Basic raycasting attributes
DEFAULT_ACTIVITY = 700
NUM_LINES = 80 # Define the number of lines and the spread angle (in degrees)
SPREAD_ANGLE = 360  # Total spread of the fan (in degrees)
ANGLE_INCREMENT = SPREAD_ANGLE / (NUM_LINES - 1) # Calculate the angle increment between each line
TILE_SIZE = 32

class Ray_Caster():
    def __init__(self, game):
        self.tiles = []
        
        self.nearby_cooldown = 0
        self.inactive_distance = 800
        
        self.game = game

        self.disable_distance_debugger = False

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
            distance = math.sqrt((self.game.player.pos[0] - tile.scaled_pos[0]) ** 2 + (self.game.player.pos[1] - tile.scaled_pos[1]) ** 2)
            
            
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
                tile.Set_Active(DEFAULT_ACTIVITY)
                self.tiles.append(tile)
            else:
                tile.Set_Active(DEFAULT_ACTIVITY)
            if not tile.type:
                print("TILE DOES NOT HAVE TYPE", tile)
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
                if not self.Check_Tile((x, y)):
                    break


    def Ray_Caster(self):
        
        self.Add_Tile_Around_Player()
        player = self.game.player
        tile_size = self.game.tilemap.tile_size

        # Calculate the starting angle
        base_angle = math.atan2(player.view_direction[1], player.view_direction[0])
        start_angle = base_angle - math.radians(SPREAD_ANGLE / 2)
        self.Check_Tile(player.tile.pos)
        
        # Look for tiles that hit the rays
        for j in range(NUM_LINES):
            angle = start_angle + j * math.radians(ANGLE_INCREMENT)
            for i in range(1, round(6 * self.game.render_scale)):
                pos_x = player.tile.pos[0] + math.cos(angle) * i
                pos_y = player.tile.pos[1] + math.sin(angle) * i
                if not self.Check_Tile((pos_x, pos_y)):
                    break
    

    def rect(self, pos):
        return pygame.Rect(pos[0], pos[1], 10, 10)
    

    def Set_Disable_Distance_Debugger(self, state):
        self.disable_distance_debugger = state