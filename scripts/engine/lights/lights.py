import math

# Managed by scripts/engine/lights/light_handler, should not be called outside there
class Light():
    _id_counter = 0  # Class variable to generate unique IDs

    def __init__(self, game, pos, light_level, tile) -> None:
        self.game = game
        self.light_level = light_level # Strength of the light
        self.pos = pos
        self.tile = tile # Tile key where the light is located
        self.tiles = [] # Tiles illuminated by this light
        self.active = True
        self.number_rays = 80 # 80 rays to balance performance and visuals
        self.field_of_view = 360

        self.id = Light._id_counter # Get unique ID for each light source
        Light._id_counter += 1  # Increment for the next light

        self.Compute_Angles()
        self.Setup_Tile_Light()

    # Light spread in a circle using cos and sin, meaning we can precompute the
    # angles of the raycaster to save performance instead of calculcating on each update
    def Compute_Angles(self):
        step = self.field_of_view / self.number_rays
        angles = [math.radians(i * step) for i in range(self.number_rays)]
        self.angle_cosines = [math.cos(angle) for angle in angles]
        self.angle_sines = [math.sin(angle) for angle in angles]

    # Check if a tile is valid
    def Check_Base_Tile(self, tile):
        if not tile:
            return False
        if not tile.translucent:
            return False
        return True
    
    def Update_Light_Level(self, new_light_level):
        self.light_level = new_light_level
    

    # Handle lighting up tiles, first checking the base tile and then using precomputed
    # angles to do raycasting from that point
    # Only called when moved for performance
    def Setup_Tile_Light(self):
        
        self.Handle_Base_Tile()

        self.Ray_Caster()
    
    def Handle_Base_Tile(self):
        # Setup the main tile under the light
        tile = self.tile
        if not self.Check_Base_Tile(tile):
            return

        # If current tile is dimmer than this light, add/update this light’s contribution
        if self.light_level > tile.light_level:
            tile.Add_Light_Contribution(self.id, self.light_level)
            self.tiles.append(tile)


    def Ray_Caster(self):
        # Start by scaling the position to the tilesize outside the loop for performance
        scaled_pos_x = self.pos[0] //  self.game.tilemap.tile_size
        scaled_pos_y = self.pos[1] // self.game.tilemap.tile_size

        # Cast rays to illuminate surrounding tiles
        for j in range(self.number_rays):
            # Fetch precomputed angles
            cos_angle = self.angle_cosines[j]
            sin_angle = self.angle_sines[j]

            for i in range(1, self.light_level + 1):

                # Calculate the ray positions in 1/32 scale 
                pos_x = scaled_pos_x + cos_angle * i
                pos_y = scaled_pos_y + sin_angle * i
                
                # Update the tile the ray is touching
                tile = self.game.tilemap.Current_Tile((pos_x, pos_y))
                if not self.Check_Base_Tile(tile):
                    break

                # Light diminishes linearly with distance, to simulate light dimming
                new_light_level = max(0, self.light_level - i)

                # Add or update contribution if it's brighter than what’s currently recorded
                # Recalculate_Light_Level on the tile will determine if it needs updating
                if new_light_level > tile.light_level:
                    tile.Add_Light_Contribution(self.id, new_light_level)
                    self.tiles.append(tile)

    
    def Delete_Light(self):
        # Remove this light's contribution from all tiles it affected
        for tile in self.tiles:
            tile.Remove_Light_Contribution(self.id)
        self.tiles.clear()
        return True
    
    def Move(self, pos, tile):
        self.Set_Pos(pos)
        self.Set_Tile(tile)

    def Set_Tile(self, tile):
        self.tile = tile

    def Set_Pos(self, pos):
        self.pos = list(pos)


    def Update_Position(self, pos):
        self.pos = list(pos)

    # Move the light source and potentially delete if the light source is no longer active
    def Move_Light(self, pos, tile_key):
        self.Set_Pos(pos)
        self.Set_Tile(tile_key)
        if not self.active:
            return
        if self.Delete_Light():
            self.Setup_Tile_Light()

    # If the light moves or changes, we can reconfigure the light
    def Update(self):
        self.Delete_Light()
        self.Setup_Tile_Light()
