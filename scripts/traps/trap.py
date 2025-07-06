from scripts.entities.entities import PhysicsEntity
from scripts.engine.keys.keys import keys

import math
import pygame
import random

class Trap(PhysicsEntity):
    def __init__(self, game, pos, size, type):
        super().__init__(game, type, 'trap', pos, size)
        self.Cooldown = 0
        self.animation = 0
        self.animation_cooldown = 0
        self.animation_max = 0
        self.ID = random.randint(1, 1000000)
        self.entity_check_cooldown = 0
        self.entities = []


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['Cooldown'] = self.Cooldown
        self.saved_data['animation'] = self.animation
        self.saved_data['animation_cooldown'] = self.animation_cooldown
        self.saved_data['animation_max'] = self.animation_max

    
    def Load_Data(self, data):
        super().Load_Data(data)
        self.Cooldown = data['Cooldown']
        self.animation = data['animation']
        self.animation_cooldown = data['animation_cooldown']
        self.animation_max = data['animation_max']

    def Update(self):
        if not self.entities:
            return False
        
        return True

    def Add_Entity_To_Trap(self, entity):
        if entity.category == keys.item:
            return False
        
        if entity in self.entities:
            return False
        
        if not self.rect().colliderect(entity.rect()):
            return False
        

        self.entities.append(entity)
        return True
    
    def Update_Cooldown(self):
        if self.entity_check_cooldown:
            self.entity_check_cooldown -= 1
            return False

        self.entity_check_cooldown = 20
        return True

    def Animation_Update(self):
        pass

    def Set_Active(self, duration):
        self.active = duration

    def Reduce_Active(self):
        self.active -= 1

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def Render(self, surf, offset=(0, 0)):

        # Get the tile surface from the assets
        tile_surface = self.game.assets[self.type][self.animation].copy()
        
        # Adjust the tile activeness calculation
        tile_activeness = max(0, min(255, 700 - self.active))
            
        # Apply a non-linear scaling for a smoother transition
        tile_darken_factor = min(255, (255 * (1 - math.exp(-tile_activeness / 255)) + 150))


     
        if self.tile.light_level > 0:
            light_level = min(255, self.tile.light_level * 25)
        else:
            light_level = 1
        tile_darken_factor = max(0, min(220, tile_darken_factor - light_level))
        
        # Create a darkening surface with an alpha channel
        darkening_surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        darkening_surface.fill((0, 0, 0, int(tile_darken_factor)))
        
        # Blit the darkening surface onto the tile surface
        tile_surface.blit(darkening_surface, (0, 0))
        
        # Blit the darkened tile surface onto the main surface
        surf.blit(tile_surface, (self.pos[0] * self.size[0] - offset[0], self.pos[1] * self.size[1] - offset[1]))


        surf.blit(tile_surface, (self.pos[0] - offset[0], self.pos[1] - offset[1]))