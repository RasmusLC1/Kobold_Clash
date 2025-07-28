import math
import pygame
from scripts.engine.keys.keys import keys

not_rendered_tiles = [keys.door_basic]

# Use dictionary keyed to pos in tilemap
class Tile():
    def __init__(self, game, type, variant, pos, size, active, light_level, physics, translucent) -> None:
        self.game = game
        self.type = type
        self.variant = variant
        self.pos = pos
        self.size = size
        self.active = active
        self.light_level = light_level
        self.max_light = 0  # Cache the max light contribution
        self.physics = physics
        self.translucent = translucent
        self.next_to_Wall = False
        self.entities = {}
        self.update_entity_cooldown = 0
        self.sprite = None
        self.needs_redraw = True  # ✅ Add flag to track if we need to redraw
        self.rendered_surface = None  # ✅ Cached surface
        self.contains_decoration = False # Flag to prevent spawning multiple decorations
        self.room = False # Flag to check if tile is part of room
        # Dictionary to hold each light's contribution
        # Key: light_id, Value: contributed_light_level
        self.light_contributions = {}
        self.Set_Sprite()

    # Use try catch to avoid loading sprites for temporary offgrid tiles
    def Set_Sprite(self):
        try:
            self.sprite = self.game.assets[self.type][self.variant].copy()
        except Exception as e:
            return
        

    def Set_Type(self, new_type):
        self.type = new_type


    def Set_Light_Level(self, new_light_level):
        self.light_level = new_light_level

    def Set_Active(self, new_active_level):
        if new_active_level != self.active:
            self.active = new_active_level
            self.needs_redraw = True

    def Set_Next_To_Wall(self, state):
        self.next_to_Wall = state

    def Set_Light_ID(self, light_id):
        self.light_ID = light_id

    def Render_All(self):
        self.Set_Light_Level(200)
        self.Set_Active(200000)

    
    def Search_Entities(self, category, ID=0):
        return [entity for entity in self.entities.values()
            if entity.category == category and entity.ID != ID]

    
    def Search_Type(self, type, ID = 0):
        return [entity for entity in self.entities.values()
                if entity.type == type and entity.ID != ID]
    
    # Update the dark level of nearby entities 
    def Set_Entity_Active(self):
        if self.update_entity_cooldown:
            self.update_entity_cooldown -= 1
            return
        for entity in self.entities.values():
            entity.Set_Active(self.active)
            entity.render_needs_update = True
            entity.Update_Dark_Surface()

        self.update_entity_cooldown = 10
        

    def Add_Entity(self, entity):
        if not entity:
            return
        self.entities[entity.ID] = entity
        entity.Set_Active(self.active)

    def Clear_Entity(self, entity_ID):
        self.entities.pop(entity_ID, None)

    def Set_Physics(self, state):
        self.physics = state
    
    def Set_Translucent(self, state):
        self.translucent = state

    def Set_Room(self, state):
        self.room = state

    def Add_Light_Contribution(self, light_id, contribution):
        # Add/update light contribution
        self.light_contributions[light_id] = contribution
        if contribution > self.max_light:
            self.max_light = contribution

        # Update max cached light level
        self.light_level = max(self.light_level, contribution)  # O(1)

    def Remove_Light_Contribution(self, light_id):
        if light_id not in self.light_contributions:
            return
        
        was_max = self.light_contributions[light_id] == self.max_light
        del self.light_contributions[light_id]

        if was_max:
            self.max_light = max(self.light_contributions.values(), default=0)
        
        # Ensure light level is also updated
        self.light_level = self.max_light

    # Recalculates the tile's visual state and caches it 
    def Update_Tile_Surface(self):
        if not self.sprite:
            return

        # Get the tile surface from the assets
        self.rendered_surface = self.sprite.copy()
        # Adjust the tile activeness calculation
        tile_activeness = max(0, min(255, 700 - self.active))
        
        # Apply a non-linear scaling for a smoother transition
        tile_darken_factor = min(255, (255 * (1 - math.exp(-tile_activeness / 255)) + 150))

        if self.light_level > 0:
            light_level = min(255, self.light_level * 25)
        else:
            light_level = 1
        tile_darken_factor = max(0, min(220, tile_darken_factor - light_level))

        # Create a darkening surface with an alpha channel
        darkening_surface = pygame.Surface(self.rendered_surface.get_size(), flags=pygame.SRCALPHA)
        darkening_surface.fill((0, 0, 0, int(tile_darken_factor)))
        
        # Blit the darkening surface onto the tile surface
        self.rendered_surface.blit(darkening_surface, (0, 0))

        self.needs_redraw = False  # Reset flag
    
    def Set_Contains_Decoration(self, state):
        self.contains_decoration = state

    # Only render active tiles from raycaster
    def Render(self, surf, offset = (0,0)):
        if not self.sprite:
            return
        if self.needs_redraw:
            self.Update_Tile_Surface() 
        # Blit the darkened tile surface onto the main surface
        surf.blit(self.rendered_surface, (self.pos[0] * self.size - offset[0], self.pos[1] * self.size - offset[1]))