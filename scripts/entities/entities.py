from collections import deque
import pygame
from scripts.engine.keys.keys import keys
from scripts.entities.entity_functions.tile_handler import TileHandler

# --- Configuration Constants ---
LIGHT_ALPHA_SCALE = 30
TILE_COOLDOWN_MAX = 0.5


class PhysicsEntity:
    _id_counter = 0
    _available_IDs = deque()

    def __init__(self, game, type, category, pos, size, sub_category=None):
        self.game = game
        self.Set_ID()
        
        # Classification
        self.category = category
        self.sub_category = sub_category
        self.type = type
        
        # Transforms & Vectors
        self.pos = pygame.Vector2(pos)
        self.size = list(size)
        
        # Rendering States
        self.sprite = None
        self.entity_image = None
        self.rendered_image = None
        self.render = True
        self.render_needs_update = True
        self.min_light_level = 40
        
        # Performance Cache Surfaces
        self._cached_dark_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        self._cached_light_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        
        # Game Logic Properties
        self.saved_data = None
        self.active = 0
        self.active_opacity = 255
        self.light_level = 0
        
        # Tile Handling Component Injection
        self.tile_handler = TileHandler(self)
        self.tile_handler.Set_Tile()
        
        self.Set_Text_Box()
        self.description = ''
        self.light_up_color = (255, 0, 0, 255)

    @property
    # Helper property to keep backward compatibility with existing code reading entity.tile
    def tile(self):
        return self.tile_handler.tile

    def Set_ID(self):
        if PhysicsEntity._available_IDs:
            self.ID = PhysicsEntity._available_IDs.popleft()
        else:
            self.ID = PhysicsEntity._id_counter
            PhysicsEntity._id_counter += 1

    def Save_Data(self):
        self.saved_data = {} 
        self.saved_data['ID'] = self.ID
        self.saved_data['category'] = self.category
        self.saved_data[keys.type] = self.type
        self.saved_data[keys.pos] = [self.pos[0], self.pos[1]]
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
        
        self.tile_handler.Set_Tile()
        
        if self.ID >= PhysicsEntity._id_counter:
            PhysicsEntity._id_counter = self.ID + 1

    def Delete(self):
        self.tile_handler.Remove_Tile()
        if hasattr(self, "ID") and self.ID not in PhysicsEntity._available_IDs:
            PhysicsEntity._available_IDs.append(self.ID)

    def rect(self):
        return pygame.Rect(self.pos, self.size)

    def Set_Active(self, duration):
        if duration == self.active:
            return
            
        self.active = duration
        self.active_opacity = max(0, min(255, duration))
        self.render_needs_update = True

    def Reduce_Active(self):
        self.Set_Active(self.active - 1)
        
    def Set_Size(self, size):
        self.size = list(size)
        self._cached_dark_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        self._cached_light_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        self.Set_Sprite()

    def Set_Position(self, position):
        try:
            self.pos = pygame.Vector2(position)
        except Exception as e:
            print(f"WRONG POSITION FORMAT: {e}", position)

    def Set_Light_Level(self, value):
        self.light_level = max(self.min_light_level, 255 - abs(value - 255))

    def Update_Light_Level(self):
        return self.tile_handler.Update_Light_Level()
        
    def Update_Tile(self, delta_time):
        return self.tile_handler.Update_Tile(delta_time)
        
    def Update_Active(self, state):
        self.Set_Active(state)
        self.Update_Dark_Surface()

    def Update_Text_Box(self, hitbox_1, hitbox_2):
        if not self.text_box:
            return None
        return self if self.text_box.Update(hitbox_1, hitbox_2) else None
        
    def Generate_Sound(self, sound_name, volume, clatter, pos=None):
        sound_pos = pos if pos else self.pos
        self.game.sound_handler.Play_Sound(sound_name, volume)
        self.game.noise_handler.Activate(sound_pos)
        if clatter:
            self.game.clatter.Generate_Clatter(sound_pos, clatter)

    def Set_Text_Box(self):
        self.text_box = None

    def Update_Dark_Surface(self):
        if not self.render_needs_update or not self.entity_image:
            return False
            
        alpha_value = max(0, min(255, self.active))
        if alpha_value == 0:
            return False
            
        try:
            self.rendered_image = self.entity_image.copy()
            self.rendered_image.set_alpha(alpha_value)
            self._cached_dark_surface.fill((self.light_level, self.light_level, self.light_level, 255))
            self.rendered_image.blit(self._cached_dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.render_needs_update = False
            return True
        except Exception as e:
            print("Error in Updating dark surface entity: ", e, self.light_level, alpha_value, self.type)
            return False

    def Lightup(self, entity_image):
        if not entity_image:
            return
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