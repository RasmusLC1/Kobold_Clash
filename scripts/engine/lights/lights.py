import math

class Light():
    _id_counter = 0

    def __init__(self, game, pos, light_level, tile) -> None:
        self.game = game
        self.light_level = light_level 
        self.pos = list(pos)
        self.tile = tile 
        self.tiles = [] 
        self.active = True
        
        # Increased ray density slightly to support sub-stepping smoothly
        self.number_rays = 120 
        self.field_of_view = 360

        self.id = Light._id_counter
        Light._id_counter += 1 

        self.Compute_Angles()
        self.Setup_Tile_Light()

    def Compute_Angles(self):
        step = self.field_of_view / self.number_rays
        rad = math.radians
        angles = [rad(i * step) for i in range(self.number_rays)]
        
        # Sub-step optimization: scale vectors down by half to double the sampling precision
        self.angle_cosines = [math.cos(a) * 0.5 for a in angles]
        self.angle_sines = [math.sin(a) * 0.5 for a in angles]

    def Setup_Tile_Light(self):
        affected_tiles = set()
        
        tile_size = self.game.tilemap.tile_size
        scaled_x = self.pos[0] / tile_size
        scaled_y = self.pos[1] / tile_size
        
        get_tile = self.game.tilemap.Current_Tile
        light_id = self.id
        base_level = self.light_level

        if self.tile and self.tile.translucent:
            if base_level > self.tile.light_level:
                self.tile.Add_Light_Contribution(light_id, base_level)
                affected_tiles.add(self.tile)

        # Loop processing using sub-stepping vectors
        for j in range(self.number_rays):
            cos_a = self.angle_cosines[j]
            sin_a = self.angle_sines[j]
            
            # Run at double density (two steps per tile unit thickness)
            for step in range(1, (base_level * 2) + 1):
                tx = scaled_x + cos_a * step
                ty = scaled_y + sin_a * step
                
                tile = get_tile((int(tx), int(ty)))
                
                if not tile or not tile.translucent:
                    break  # Solid barrier hit safely, stopping light leak
                
                # True Euclidean Distance Radial Decay Formula
                distance = math.hypot(tx - scaled_x, ty - scaled_y)
                new_level = int(base_level - distance)
                
                if new_level <= 0:
                    break
                
                if new_level > tile.light_level:
                    tile.Add_Light_Contribution(light_id, new_level)
                    affected_tiles.add(tile)
        
        self.tiles = list(affected_tiles)

    def Delete_Light(self):
        if not self.tiles:
            return False
        for tile in self.tiles:
            tile.Remove_Light_Contribution(self.id)
        self.tiles.clear()
        return True

    def Move_Light(self, pos, tile):
        self.pos = list(pos)
        self.tile = tile
        if self.active:
            self.Reset_Light()
    
    def Reset_Light(self):
        self.Delete_Light()
        self.Setup_Tile_Light()

    def Update_Light_Level(self, light_level):
        self.light_level = light_level
        self.Reset_Light()