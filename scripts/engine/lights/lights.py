import math

class Light():
    _id_counter = 0

    def __init__(self, game, pos, light_level, tile) -> None:
        self.game = game
        self.light_level = light_level 
        self.pos = list(pos)
        self.tile = tile 
        self.tiles = [] # Now stored as a list of unique tiles
        self.active = True
        self.number_rays = 80 
        self.field_of_view = 360

        self.id = Light._id_counter
        Light._id_counter += 1 

        self.Compute_Angles()
        self.Setup_Tile_Light()

    def Compute_Angles(self):
        step = self.field_of_view / self.number_rays
        # Localizing math.radians for a tiny speed boost during setup
        rad = math.radians
        angles = [rad(i * step) for i in range(self.number_rays)]
        self.angle_cosines = [math.cos(a) for a in angles]
        self.angle_sines = [math.sin(a) for a in angles]

    def Setup_Tile_Light(self):
        # Use a temporary set to ensure we don't track the same tile multiple times
        affected_tiles = set()
        
        # Localize variables for the hot loop
        tile_size = self.game.tilemap.tile_size
        scaled_x = self.pos[0] // tile_size
        scaled_y = self.pos[1] // tile_size
        
        get_tile = self.game.tilemap.Current_Tile
        light_id = self.id
        base_level = self.light_level

        # Handle Base Tile
        if self.tile and self.tile.translucent:
            if base_level > self.tile.light_level:
                self.tile.Add_Light_Contribution(light_id, base_level)
                affected_tiles.add(self.tile)

        # Raycasting
        for j in range(self.number_rays):
            cos_a = self.angle_cosines[j]
            sin_a = self.angle_sines[j]

            for i in range(1, base_level + 1):
                tx = scaled_x + cos_a * i
                ty = scaled_y + sin_a * i
                
                tile = get_tile((tx, ty))
                
                # Check if light is blocked
                if not tile or not tile.translucent:
                    break

                new_level = base_level - i
                
                # Only update if this light is actually contributing something brighter
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

    # Moves and updates only this light
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
