import math
import pygame
from scripts.engine.keys.keys import keys

not_rendered_tiles = [keys.door_basic]
TILE_SIZE = 32

# Use dictionary keyed to pos in tilemap
class Tile():
    def __init__(self, game, type, sub_type, variant, pos, active, light_level, physics, translucent) -> None:
        self.game = game
        self.saved_data = {}
        self.type = type
        self.sub_type = sub_type
        self.variant = variant
        self.pos = pos # Tile coordinates
        self.scaled_pos = (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE) # Scaled size 
        self.size = 32
        self.active = active
        self.light_level = light_level
        self.max_light = 0  # Cache the max light contribution
        self.physics = physics
        self.translucent = translucent
        self.next_to_Wall = False
        self.entities = {}
        self.update_entity_cooldown = 0
        self.sprite = None
        self.needs_redraw = True  # Add flag to track if we need to redraw
        self.rendered_surface = None  # Cached surface
        self.contains_decoration = False # Flag to prevent spawning multiple decorations
        self.room = False # Flag to check if tile is part of room
        self.trap = False # Flag to check if tile contains trap
        self.minimap = False # Flag if the tile has been added to the minimap
        self.distance_to_player = (999,999)
        self.last_distance_update_timestamp = 0
        # Dictionary to hold each light's contribution
        # Key: light_id, Value: contributed_light_level
        self.light_contributions = {}
        self.Set_Sprite()

    # Use try catch to avoid loading sprites for temporary offgrid tiles
    def Set_Sprite(self):
        try:
            self.sprite = self.game.assets[self.sub_type][self.variant].copy()
        except Exception as e:
            return

    def Save_Data(self):
        self.saved_data[keys.type] = self.type
        self.saved_data[keys.sub_type] = self.sub_type
        self.saved_data[keys.variant] = self.variant
        self.saved_data[keys.pos] = self.pos
        self.saved_data["scaled_pos"] = self.scaled_pos
        self.saved_data["active"] = self.active
        self.saved_data["light_level"] = self.light_level
        self.saved_data["max_light"] = self.max_light
        self.saved_data["translucent"] = self.translucent
        self.saved_data["next_to_Wall"] = self.next_to_Wall
        self.saved_data["light_contributions"] = self.light_contributions


    def Load_Data(self, data):
        if not data:
            return
        
        self.type = data[keys.type] 
        self.sub_type = data[keys.sub_type] 
        self.variant = data[keys.variant] 
        self.scaled_pos = data["scaled_pos"] 
        self.active = data["active"] 
        self.light_level = data["light_level"] 
        self.max_light = data["max_light"] 
        self.translucent = data["translucent"] 
        self.next_to_Wall = data["next_to_Wall"] 
        self.light_contributions = data["light_contributions"]
        self.needs_redraw = True
        self.Set_Sprite()


# ENTITY LOGIC    
    def Search_Entities(self, category, ID=0):
        return [entity for entity in self.entities.values()
            if entity.category in (category) and entity.ID != ID]

    
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
    
    # Sets an entity based on the entity ID 
    def Add_Entity(self, entity):
        if not entity:
            return
        self.entities[entity.ID] = entity
        entity.Set_Active(self.active)

    def Clear_Entity(self, entity_ID):
        self.entities.pop(entity_ID, None)

    # Calculates distance to player after 0.5 second
    # return distance to player
    def Get_Distance_To_Player(self):
        if self.game.total_time - self.last_distance_update_timestamp > 0.5:
            self.Calculate_Distance_To_Player()

        return self.distance_to_player

    # Uses squared distance to palyer for optimisation
    # Stores the time stamp of the calculation for comparison
    def Calculate_Distance_To_Player(self):
        player_pos = self.game.player.pos
        dx = self.scaled_pos[0]  - player_pos[0]
        dy = self.scaled_pos[1]  - player_pos[1]
        self.distance_to_player = dx * dx + dy * dy
        self.last_distance_update_timestamp = self.game.total_time

  
# SET FUNCTIONS
    def Set_Physics(self, state):
        self.physics = state
    
    def Set_Translucent(self, state):
        self.translucent = state

    def Set_Room(self, state):
        self.room = state

    def Set_Trap(self, state):
        self.trap = state

    def Add_To_Minimap(self):
        # If already added to minimap return false
        if self.minimap:
            return False
        
        self.minimap = True
        return True
    
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

# LIGHT LOGIC
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


    def Set_Contains_Decoration(self, state):
        self.contains_decoration = state

# RENDER LOGIC

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
    
    

    # Only render active tiles from raycaster
    def Render(self, surf, offset = (0,0)):
        if not self.sprite:
            return
        if self.needs_redraw:
            self.Update_Tile_Surface() 
        # Blit the darkened tile surface onto the main surface
        surf.blit(self.rendered_surface, (self.pos[0] * self.size - offset[0], self.pos[1] * self.size - offset[1]))

    # Used to render the minimap
    def Render_Minimap(self, surf, minimap_pos):
        # Determine color based on tile type
        color = (100, 100, 100) # Default Gray
        if self.physics: # It's a wall
            color = (200, 200, 200) # Light Gray/White

        # TODO: Add item to detect traps
        # if self.game.player.trap_detection:
        #   if self.trap:
        #     color = (255, 50, 50) # Red
        
        # Draw a small rectangle representing the tile, performant
        pygame.draw.rect(surf, color, (minimap_pos[0], minimap_pos[1], 2, 2))