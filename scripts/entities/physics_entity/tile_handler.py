import pygame

LIGHT_ALPHA_SCALE = 30
TILE_COOLDOWN_MAX = 0.5

class Tile_Handler:
    def __init__(self, entity):
        self.entity = entity
        self.game = entity.game
        self.tile = None
        self.update_tile_cooldown = 0.0

    def Set_Tile(self):
        self.Remove_Tile()
        
        tile_size = self.game.tilemap.tile_size
        tx = int(self.entity.pos[0]) // tile_size
        ty = int(self.entity.pos[1]) // tile_size
        
        new_tile = self.game.tilemap.Current_Tile((tx, ty))
        if not new_tile:
            # If the specific target tile doesn't exist yet, try finding an absolute structural tile link 
            return self._Check_If_Tile()
            
        self.tile = new_tile
        
        # Route safely into the unified components API
        if hasattr(self.tile, 'Add_Entity'):
            self.tile.Add_Entity(self.entity)
        else:
            self.game.tilemap.Add_Entity_To_Tile(self.tile, self.entity)
        return True

    def Remove_Tile(self):
        if not self.tile:
            return
        if hasattr(self.tile, 'Remove_Entity'):
            self.tile.Remove_Entity(self.entity.ID)
        else:
            self.game.tilemap.Remove_Entity_From_Tile(self.tile, self.entity.ID)
        self.tile = None

    def Update_Light_Level(self):
        if not self.tile:
            return True

        target_light = min(255, self.tile.light_level * LIGHT_ALPHA_SCALE)

        if self.entity.light_level < target_light:
            self.entity.Set_Light_Level(self.entity.light_level + 5)
        elif self.entity.light_level > target_light:
            self.entity.Set_Light_Level(self.entity.light_level - 5)
        
        return self.entity.light_level > self.entity.min_light_level

    def Update_Tile_Cooldown(self, delta_time):
        if self.update_tile_cooldown > 0:
            self.update_tile_cooldown -= delta_time
            return False

        self.update_tile_cooldown = TILE_COOLDOWN_MAX
        return True
        
    def Update_Tile(self, delta_time):
        if not self.Update_Tile_Cooldown(delta_time):
            return False

        if not self._Check_If_Tile():
            return False    

        t_size = self.game.tilemap.tile_size
        nx, ny = int(self.entity.pos[0]) // t_size, int(self.entity.pos[1]) // t_size

        if (nx, ny) == self.tile.pos:
            return False

        return self._Add_New_Tile(nx, ny)
    
    def _Add_New_Tile(self, nx, ny):
        new_tile = self.game.tilemap.Current_Tile((nx, ny))
        
        if new_tile and new_tile != self.tile:
            self.Remove_Tile()
            self.tile = new_tile
            if hasattr(self.tile, 'Add_Entity'):
                self.tile.Add_Entity(self.entity)
            else:
                self.game.tilemap.Add_Entity_To_Tile(self.tile, self.entity)
            return True
        
        return False
    
    def _Check_If_Tile(self):
        if self.tile:
            return True
        
        # Pull a safe floor backup position vector
        new_tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
        if not new_tile:
            self.entity.Delete()
            return False
        
        self.tile = new_tile
        self.entity.Set_Position(self.tile.scaled_pos)
        
        self.tile.Add_Entity(self.entity)
        return True