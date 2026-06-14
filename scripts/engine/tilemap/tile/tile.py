import pygame
from scripts.engine.keys.keys import keys
from .tile_lightning import Tile_Lighting
from .tile_navigation import Tile_Navigation
from .tile_renderer import Tile_Renderer
from .tile_entity_handler import Tile_Entity_Handler
import math

TILE_SIZE = 32

class Tile:
    # REMOVED: 'light_level', 'max_light', 'distance_to_player', 'entities'
    # These must be managed purely by property decorators!
    __slots__ = [
        'game', 'saved_data', 'type', 'sub_type', 'variant', 'pos', 'scaled_pos',
        'size', 'active', 'physics', 'touching_wall', 'translucent',
        'neighbor_tiles', 'neighbor_physics_rects', 'needs_redraw', 
        'contains_decoration', 'room', 'trap', 'minimap', 'hitbox',
        'lighting', 'renderer', 'navigation', 'entity_handler'
    ]

    def __init__(self, game, type, sub_type, variant, pos, active, light_level, physics, translucent) -> None:
        self.game = game
        self.saved_data = None
        self.type = type
        self.sub_type = sub_type
        self.variant = variant
        self.pos = pos
        self.scaled_pos = (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
        self.size = TILE_SIZE
        self.active = active
        self.touching_wall = False
        self.translucent = translucent
        
        self.neighbor_tiles = []
        self.neighbor_physics_rects = []
        self.needs_redraw = True
        self.contains_decoration = False
        self.room = False
        self.trap = None
        self.minimap = False

        # --- Component Injection ---
        self.lighting = Tile_Lighting(self, light_level)
        self.renderer = Tile_Renderer(self)
        self.navigation = Tile_Navigation(self)
        self.entity_handler = Tile_Entity_Handler(self) 

        self.Set_Physics(physics)

    # --- Properties for Backward Compatibility ---
    @property
    def light_level(self):
        return self.lighting.light_level

    @light_level.setter
    def light_level(self, val):
        self.lighting.light_level = val

    @property
    def max_light(self):
        return self.lighting.max_light

    @property
    def distance_to_player(self):
        return self.navigation.distance_to_player
    
    @property
    def entities(self):
        """Allows legacy code like `tile.entities.values()` to work seamlessly."""
        return self.entity_handler.entities

    # --- Delegated Entity API ---
    def Add_Entity(self, entity):
        self.entity_handler.Add_Entity(entity)

    def Remove_Entity(self, entity_ID):
        self.entity_handler.Remove_Entity(entity_ID)

    def Set_Entity_Active(self, delta_time):
        self.entity_handler.Set_Entity_Active(delta_time)

    def Search_Entities(self, category, ID=0):
        return self.entity_handler.Search_Entities(category, ID)

    def Search_Type(self, type, ID=0):
        return self.entity_handler.Search_Type(type, ID)
    
    # --- Delegated Lighting API ---
    def Add_Light_Contribution(self, light_id, contribution):
        self.lighting.Add_Contribution(light_id, contribution)

    def Remove_Light_Contribution(self, light_id):
        self.lighting.Remove_Contribution(light_id)

    # --- Setter Functions ---
    def Set_Touching_Wall(self):
        self.touching_wall = True

    def Set_Translucent(self, state):
        self.translucent = state

    def Set_Room(self, state):
        self.room = state

    def Set_Trap(self, trap):
        self.trap = trap

    def Set_Type(self, new_type):
        self.type = new_type

    def Set_Light_ID(self, light_id):
        self.lighting.light_ID = light_id

    def Set_Contains_Decoration(self, state):
        self.contains_decoration = state

    def Add_To_Minimap(self):
        if self.minimap:
            return False
        self.minimap = True
        return True

# --- Core Mechanics API ---
    def Set_Physics(self, state):
        self.physics = state
        self.hitbox = pygame.Rect(self.scaled_pos[0], self.scaled_pos[1], TILE_SIZE, TILE_SIZE) if state else None

    def Set_Active(self, new_active_level):
        if new_active_level != self.active:
            self.active = new_active_level
            self.needs_redraw = True


    def Render(self, surf, offset = (0,0)):
        self.renderer.Render(surf, offset)

    def Render_Minimap(self, surf, minimap_pos):
        color = (200, 200, 200) if self.physics else (100, 100, 100)
        pygame.draw.rect(surf, color, (minimap_pos[0], minimap_pos[1], 2, 2))


    def Save_Data(self):
        self.saved_data = {
            keys.type: self.type,
            keys.sub_type: self.sub_type,
            keys.variant: self.variant,
            keys.pos: self.pos,
            "scaled_pos": self.scaled_pos,
            "active": self.active,
            "light_level": self.lighting.light_level,
            "max_light": self.lighting.max_light,
            "translucent": self.translucent,
            "touching_wall": self.touching_wall,
            "light_contributions": self.lighting.light_contributions
        }
        return self.saved_data

    def Load_Data(self, data):
        if not data: 
            return
        self.type = data[keys.type]
        self.sub_type = data[keys.sub_type]
        self.variant = data[keys.variant]
        self.scaled_pos = data["scaled_pos"]
        self.active = data["active"]
        self.translucent = data["translucent"]
        self.touching_wall = data["touching_wall"]
        
        self.lighting.light_level = data["light_level"]
        self.lighting.max_light = data["max_light"]
        self.lighting.light_contributions = data["light_contributions"]
        
        self.needs_redraw = True
        self.renderer.Set_Sprite()