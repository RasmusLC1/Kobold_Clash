import pygame
from collections import deque
from scripts.engine.keys.keys import keys

class PhysicsEntity:
    _id_counter = 0  # Class variable to generate unique IDs
    _available_IDs = deque() # List of ID's made available on deletion, deque for performance

    def __init__(self, game, type, category, pos, size, sub_category = None):
        self.game = game
        self.Set_ID()
        self.category = category # Category = Potion, enemy, player, etc
        self.sub_category = sub_category # Subcategory = variant of the category item -> weapon item 
        self.type = type # Type = Specific type of entity
        self.sprite = None # The type of animation used
        self.entity_image = None # the full animation with animation frame
        self.rendered_image = None # the actual image being rendered to screen
        self.render_needs_update = True
        self.pos = list(pos)
        self.size = size
        self.active = 0
        self.light_level = 0
        self.render = True
        self.Set_Tile()
        self.saved_data = {}
        self.text_box = None
        self.description = ''
        self.light_up_color = (255, 0, 0, 255)


    def Save_Data(self):
        self.saved_data['category'] = self.category
        self.saved_data[keys.type] = self.type
        self.saved_data[keys.pos] = self.pos
        self.saved_data['size'] = self.size
        self.saved_data['active'] = self.active
        self.saved_data['light_level'] = self.light_level
        self.saved_data['render'] = self.render

    
    def Load_Data(self, data):
        self.category = data['category']
        self.type = data[keys.type]
        self.pos = data[keys.pos]
        self.size = data['size']
        self.active = data['active']
        self.light_level = data['light_level']
        self.render = data['render']
        self.Set_Tile()


    # Should only be called during initalisation
    def Set_ID(self):
        if PhysicsEntity._available_IDs:
            self.ID = PhysicsEntity._available_IDs.popleft()  # Take the oldest available ID
        else:
            self.ID = PhysicsEntity._id_counter
            PhysicsEntity._id_counter += 1


    # Called when entity is deleted by garbage collection
    def __del__(self):
        if not hasattr(self, "ID"):
            return
        PhysicsEntity._available_IDs.append(self.ID)

    # Called when entity is deleted
    # Manually deletes the entity and returns the ID to the pool
    def Delete(self):
        PhysicsEntity._available_IDs.append(self.ID)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def Set_Active(self, duration):
        if duration != self.active:
            self.active = duration
            self.render_needs_update = True
            

    def Reduce_Active(self):
        self.active -= 1

        
    def Update(self):
        pass

    def Damage_Taken(self, damage):
        pass

    def Set_Effect(self, effect, duration, permanent = False):
        pass

    def Set_Size(self, size):
        self.size = size
        self.Set_Sprite() # Image needs to be resized
    
    def Set_Tile(self):
        tile_key = str(int(self.pos[0]) // self.game.tilemap.tile_size) + ';' + str(int(self.pos[1]) // self.game.tilemap.tile_size)
        self.tile = self.game.tilemap.Current_Tile(tile_key)
        if not self.tile:
            return
        self.game.tilemap.Add_Entity_To_Tile(self.tile, self)
        
        self.tile.Add_Entity(self)

    def Remove_Tile(self):
        if not self.tile:
            return
        self.game.tilemap.Remove_Entity_From_Tile(self.tile, self.ID)
        self.tile = None

    def Set_Position(self, position):
        self.pos = position

    def Set_Sprite(self):
        pass

    # Setting the item image and scaling it
    def Set_Entity_Image(self):
        pass

    def Set_Light_Level(self, value):
        self.light_level = value

    def Update_Light_Level(self):
        # Set the light level based on the tile that the entity is placed on
        tile = self.tile
        if not tile:
            return True
        if not self.light_level:
            self.light_level = 0
        if tile.light_level == self.light_level:
            return True
        new_light_level = min(255, tile.light_level * 30)
        if self.light_level < new_light_level:
            self.Set_Light_Level(self.light_level + 5)
        elif self.light_level > new_light_level:
            self.Set_Light_Level(self.light_level - 5)
        self.light_level = abs(self.light_level - 255)
        # 75 is the darkest level we want
        self.light_level = max(40, 255 - self.light_level)
        

        if self.light_level <= 40:
            return False
        else:
            return True
    
    def Set_Description(self):
        pass

    def Update_Text_Box(self, hitbox_1, hitbox_2):
        if not self.text_box:
            return None
        if self.text_box.Update(hitbox_1, hitbox_2):
            return self
        else:
            return None
        
    def Generate_Sound(self, sound_name, volume):
        self.game.sound_handler.Play_Sound(sound_name, volume)
        self.game.noise_handler.Activate(self.pos)

    def Render(self, surf, offset=(0, 0)):
        pass

    def Update_Dark_Surface(self):
        if not self.render_needs_update:
            return
        if not self.entity_image:
            return
        alpha_value = max(0, min(255, self.active))  # Adjust the factor as needed
        if not alpha_value:
            return
        try:
            # Set image
            self.rendered_image = self.entity_image.copy()
            self.rendered_image.set_alpha(alpha_value)

            # Blit the dark layer
            dark_surface_head = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
            dark_surface_head.fill((self.light_level, self.light_level, self.light_level, 255))

            # Blit the chest layer on top the dark layer
            self.rendered_image.blit(dark_surface_head, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.render_needs_update = False
        except Exception as e:
            print("Error in Updating dark surface entity: ", e, dark_surface_head, self.light_level, alpha_value, self.type)


    def Lightup(self, entity_image):
        
        # Blit the dark layer
        light_up_surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
        light_up_surface.fill(self.light_up_color)
        # Blit the chest layer on top the dark layer
        if not light_up_surface or not entity_image:
            return
        entity_image.blit(light_up_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)