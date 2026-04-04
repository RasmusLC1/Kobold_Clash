import math
import pygame
from scripts.engine.keys.keys import keys

# Basic raycasting attributes
DEFAULT_ACTIVITY = 700
NUM_LINES = 100 # Define the number of lines and the spread angle (in degrees)
SPREAD_ANGLE = 360  # Total spread of the fan (in degrees)
ANGLE_INCREMENT = SPREAD_ANGLE / (NUM_LINES - 1) # Calculate the angle increment between each line
TILE_SIZE = 32
INACTIVE_DISTANCE = 800 * 800

class Ray_Caster():
    def __init__(self, game):
        self.tiles = []
        self.nearby_cooldown = 0
        self.saved_data = None
        self.game = game

        self.disable_distance_debugger = False

        self.angles = []

    def Save_Data(self):
        self.saved_data = {}
        tilemap = self.game.tilemap
        for tile in self.tiles:
            # Get the string key for the dictionary
            tile_key = tilemap.Convert_Tile_Pos_To_Key(tile.pos)
            # Store the position. Note: JSON will turn this tuple into a list [x, y]
            self.saved_data[tile_key] = tile.pos

    def Load_Data(self, data):
        # data is a dict where values are like [109, 104]
        for pos_data in data.values():
            # Ensure the position is a tuple, not a list
            tile_key = tuple(pos_data) 
            
            tile = self.game.tilemap.Get_Tile(tile_key)
            
            if not tile:
                print(f"RAYCASTER TILE NOT FOUND AT {tile_key}")
                continue
                
            self.tiles.append(tile)



    def Update(self, delta_time):
        if self.disable_distance_debugger:
            return
        
        self.Check_Tile_Active()

        self.Update_Entities(delta_time)


    def Update_Entities(self, delta_time):
        for tile in self.tiles:
            tile.Set_Entity_Active(delta_time)

    # Handle tile activity degradation
    def Check_Tile_Active(self):
        player_pos = self.game.player.pos
        for tile in self.tiles:
            if tile.active:
                tile.active -= 1
            # Find distance from player and if it's greater than 300, delete it
            # distance = math.sqrt((self.game.player.pos[0] - tile.scaled_pos[0]) ** 2 + (self.game.player.pos[1] - tile.scaled_pos[1]) ** 2)
            distance = self.Calculate_Distance(player_pos, tile)
            
            if distance > INACTIVE_DISTANCE:
                tile.active = 0
                self.tiles.remove(tile)
    
    def Calculate_Distance(self, player_pos, tile):
        dx = player_pos[0] - tile.scaled_pos[0]
        dy = player_pos[1] - tile.scaled_pos[1]
        distance = dx * dx + dy * dy
        return distance

    def Remove_Tile(self, tile):
        if tile not in self.tiles:
            return
        tile.active = 0
        self.tiles.remove(tile)


    def Check_Tile(self, tile):
        tilemap = self.game.tilemap
        tile = tilemap.Current_Tile(tile)
        if not tile:
            return False
        
        if not tile.active:
            self.Add_Tile(tilemap, tile)
        else:
            tile.Set_Active(DEFAULT_ACTIVITY)
        
        if not tile.translucent:
            return False
            
            
        return True

    # Logic for adding tile to the active tiles
    def Add_Tile(self, tilemap, tile):
        tile.Set_Active(DEFAULT_ACTIVITY)
        self.tiles.append(tile)
        tilemap.Add_Tile_To_Minimap(tile) # Try to add tile

    def Clear_Entity_From_Tiles(self, entity_ID):
        for tile in self.tiles:
            tile.Clear_Entity(entity_ID)
 
    def Ray_Caster(self):
        
        player = self.game.player
        player_tile_pos = player.tile.pos

        # Calculate the starting angle
        base_angle = math.atan2(0, 0)
        start_angle = base_angle - math.radians(SPREAD_ANGLE / 2)
        self.Check_Tile(player_tile_pos)
        # Look for tiles that hit the rays
        for j in range(NUM_LINES):
            angle = start_angle + j * math.radians(ANGLE_INCREMENT)
            for i in range(1, round(8 * self.game.render_scale)):
                pos_x = player_tile_pos[0] + math.cos(angle) * i
                pos_y = player_tile_pos[1] + math.sin(angle) * i
                if not self.Check_Tile((pos_x, pos_y)):
                    break
    

    def rect(self, pos):
        return pygame.Rect(pos[0], pos[1], 10, 10)
    

    def Set_Disable_Distance_Debugger(self, state):
        self.disable_distance_debugger = state