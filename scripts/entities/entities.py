from collections import deque
import pygame
from scripts.engine.keys.keys import keys

# --- Configuration Constants ---
MIN_LIGHT_LEVEL = 40
LIGHT_ALPHA_SCALE = 30
TILE_COOLDOWN_MAX = 0.5


class PhysicsEntity:
    _id_counter = 0  # Class variable to generate unique IDs
    _available_IDs = deque()  # List of ID's made available on deletion, deque for performance

    def __init__(self, game, type, category, pos, size, sub_category=None):
        self.game = game
        self.Set_ID()
        
        # Classification
        self.category = category  # Category = Potion, enemy, player, etc
        self.sub_category = sub_category  # Subcategory = variant of the category item -> weapon item 
        self.type = type  # Type = Specific type of entity
        
        # Transforms & Vectors
        self.pos = pygame.Vector2(pos)  # Converted to Vector2 internally for performance, fully compatible with list/tuple inputs
        self.size = list(size)
        
        # Rendering States
        self.sprite = None  # The type of animation used
        self.entity_image = None  # the full animation with animation frame
        self.rendered_image = None  # the actual image being rendered to screen
        self.render = True
        self.render_needs_update = True
        
        # Performance Cache Surfaces: Allocating once here prevents severe frame drops during gameplay
        self._cached_dark_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        self._cached_light_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        
        # Game Logic Properties
        self.saved_data = None
        self.update_tile_cooldown = 0.0
        self.active = 0
        self.active_opacity = 255  # Fixed typo from actiactivee_opacity
        self.light_level = 0  # Range from 0 to 255, 0 being low
        self.tile = None
        
        self.Set_Tile()
        self.Set_Text_Box()
        self.description = ''
        self.light_up_color = (255, 0, 0, 255)

    def Set_ID(self):
        """Should only be called during initialization."""
        if PhysicsEntity._available_IDs:
            self.ID = PhysicsEntity._available_IDs.popleft()  # Take the oldest available ID
        else:
            self.ID = PhysicsEntity._id_counter
            PhysicsEntity._id_counter += 1

    def Save_Data(self):
        """Initialise inside save function to prevent loading empty arrays for every entity."""
        self.saved_data = {} 
        self.saved_data['ID'] = self.ID
        self.saved_data['category'] = self.category
        self.saved_data[keys.type] = self.type
        self.saved_data[keys.pos] = [self.pos.x, self.pos.y]  # Exported as list for standard JSON/Data serialization
        self.saved_data['size'] = self.size
        self.saved_data['active'] = self.active
        self.saved_data['light_level'] = self.light_level
        self.saved_data['render'] = self.render

    def Load_Data(self, data):
        self.ID = data['ID']
        self.category = data['category']
        self.type = data[keys.type]
        self.pos = pygame.Vector2(data[keys.pos])
        self.size = data['size']
        self.active = data['active']
        self.light_level = data['light_level']
        self.render = data['render']
        
        self.Set_Tile()
        
        # Safely align counter past loaded historical maximums to prevent ID overlaps
        if self.ID >= PhysicsEntity._id_counter:
            PhysicsEntity._id_counter = self.ID + 1

    def Delete(self):
        """Manually deletes the entity, cleans up spatial grids, and returns the ID to the pool."""
        self.Remove_Tile()
        if hasattr(self, "ID") and self.ID not in PhysicsEntity._available_IDs:
            PhysicsEntity._available_IDs.append(self.ID)

    def rect(self):
        # Passing the Vector2 object directly to Rect avoids slow Python-side attribute lookups
        return pygame.Rect(self.pos, self.size)

    def Set_Active(self, duration):
        """Sets the active state duration and flags the render state for an update."""
        if duration == self.active:
            return
            
        self.active = duration  # Restored assignment missing from original version
        self.active_opacity = max(0, min(255, duration))  # Fixed variable typo
        self.render_needs_update = True

    def Reduce_Active(self):
        self.Set_Active(self.active - 1)
        
    def Set_Size(self, size):
        self.size = list(size)
        # Re-cache scratch surfaces to match the new dimensions safely
        self._cached_dark_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        self._cached_light_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        self.Set_Sprite()  # Image needs to be resized
    
    def Set_Tile(self):
        self.Remove_Tile()  # Clear existing positions cleanly first
        
        tile_size = self.game.tilemap.tile_size
        tx = int(self.pos.x) // tile_size
        ty = int(self.pos.y) // tile_size
        
        new_tile = self.game.tilemap.Current_Tile((tx, ty))
        if not new_tile:
            return False
            
        self.tile = new_tile
        self.game.tilemap.Add_Entity_To_Tile(self.tile, self)
        
        if hasattr(self.tile, 'Add_Entity'):
            self.tile.Add_Entity(self)
        return True

    def Remove_Tile(self):
        if self.tile:
            self.game.tilemap.Remove_Entity_From_Tile(self.tile, self.ID)
            if hasattr(self.tile, 'Remove_Entity'):
                self.tile.Remove_Entity(self)
            self.tile = None

    def Set_Position(self, position):
        try:
            self.pos = pygame.Vector2(position)
        except Exception as e:
                print(f"WRONG POSITION FORMAT: {e}", position)

    def Set_Light_Level(self, value):
        # Normalize light level: 255 = full light, 40 = minimum visible
        self.light_level = max(MIN_LIGHT_LEVEL, 255 - abs(value - 255))

    def Update_Light_Level(self):
        # Set the light level based on the tile that the entity is placed on
        if not self.tile:
            return True

        new_light_level = min(255, self.tile.light_level * LIGHT_ALPHA_SCALE)

        # Responsible for gradual fade in/out to prevent sudden light changes
        if self.light_level < new_light_level:
            self.Set_Light_Level(self.light_level + 5)
            self.render_needs_update = True
        elif self.light_level > new_light_level:
            self.Set_Light_Level(self.light_level - 5)
            self.render_needs_update = True
        
        return self.light_level > MIN_LIGHT_LEVEL
    
    def Update_Active(self, state):
        self.Set_Active(state)
        self.Update_Dark_Surface()

    def Update_Text_Box(self, hitbox_1, hitbox_2):
        if not self.text_box:
            return None
        return self if self.text_box.Update(hitbox_1, hitbox_2) else None
        
    def Update_Tile_Cooldown(self, delta_time):
        if self.update_tile_cooldown > 0:
            self.update_tile_cooldown -= delta_time
            return False

        self.update_tile_cooldown = TILE_COOLDOWN_MAX
        return True
        
    def Update_Tile(self, delta_time):
        # Cooldown check - prevents running heavy logic every frame
        if not self.Update_Tile_Cooldown(delta_time):
            return False

        if not self._Check_If_Tile():
            return False    

        t_size = self.game.tilemap.tile_size
        nx, ny = int(self.pos.x) // t_size, int(self.pos.y) // t_size

        # Exit early if coordinates haven't changed tiles
        if (nx, ny) == self.tile.pos:
            return False

        return self._Add_New_Tile(nx, ny)
    
    def _Add_New_Tile(self, nx, ny):
        new_tile = self.game.tilemap.Current_Tile((nx, ny))
        
        if new_tile and new_tile != self.tile:
            self.Remove_Tile()
            self.tile = new_tile
            self.game.tilemap.Add_Entity_To_Tile(self.tile, self)
            if hasattr(self.tile, 'Add_Entity'):
                self.tile.Add_Entity(self)
            return True
        
        return False
    
    def _Check_If_Tile(self):
        # Recovery: If the entity has no tile, teleport it to a valid one
        if self.tile:
            return True
        
        print(f"ERROR TILE NOT FOUND: {self.type} at {self.pos}")
        new_tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
        if not new_tile:
            self.Delete()  # Delete if out of bounds
            return False
        
        self.tile = new_tile
        self.pos = pygame.Vector2(self.tile.scaled_pos)
        self.game.tilemap.Add_Entity_To_Tile(self.tile, self)
        if hasattr(self.tile, 'Add_Entity'):
            self.tile.Add_Entity(self)
        return True
        
    def Generate_Sound(self, sound_name, volume, clatter, pos=None):
        sound_pos = pos if pos else self.pos
        self.game.sound_handler.Play_Sound(sound_name, volume)
        self.game.noise_handler.Activate(sound_pos)
        if clatter:
            self.game.clatter.Generate_Clatter(sound_pos, clatter)  # Generate clatter to alert nearby enemies

    def Set_Text_Box(self):
        self.text_box = None

    def Update_Dark_Surface(self):
        if not self.render_needs_update or not self.entity_image:
            return False
            
        alpha_value = max(0, min(255, self.active))
        if alpha_value == 0:
            return False
            
        try:
            # Set image
            self.rendered_image = self.entity_image.copy()
            self.rendered_image.set_alpha(alpha_value)

            # Reuse cached dark surface layer instead of instantiating surfaces continuously
            self._cached_dark_surface.fill((self.light_level, self.light_level, self.light_level, 255))

            # Blit the layer on top using color multiplication
            self.rendered_image.blit(self._cached_dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.render_needs_update = False
            return True
        except Exception as e:
            print("Error in Updating dark surface entity: ", e, self.light_level, alpha_value, self.type)
            return False

    def Lightup(self, entity_image):
        if not entity_image:
            return
        # Use the structural cached light surface vector to process opacity variations cleanly
        self._cached_light_surface.fill(self.light_up_color)
        entity_image.blit(self._cached_light_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # --- Stubs for Child Extensions ---
    def Update(self, delta_time): pass
    def Damage_Taken(self, damage): pass
    def Set_Effect(self, effect, duration, permanent=False): pass
    def Set_Sprite(self): pass
    def Set_Entity_Image(self): pass
    def Set_Description(self): pass
    def Render(self, surf, offset=(0, 0)): pass