from scripts.entities.entity.entities import PhysicsEntity
from scripts.engine.keys.keys import keys

import math
import pygame
import random

COOLDOWN_MAX = 0.05
DAMAGE_COOLDOWN = 1

class Trap(PhysicsEntity):
    def __init__(self, game, pos, type, size = (32, 32)):
        super().__init__(game, type, 'trap', pos, size)
        self.cooldown = 0
        self.animation = 0
        self.Set_Sprite()
        self.animation_cooldown = 0
        self.animation_max = 0
        self.entity_check_cooldown = 0
        self.entities = {}
        if self.tile:
            self.tile.Set_Trap(self)
        self.damaged_entities = {}


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['Cooldown'] = self.cooldown
        self.saved_data['animation'] = self.animation
        self.saved_data['animation_cooldown'] = self.animation_cooldown
        self.saved_data['animation_max'] = self.animation_max

    
    def Load_Data(self, data):
        super().Load_Data(data)
        self.cooldown = data['Cooldown']
        self.animation = data['animation']
        self.animation_cooldown = data['animation_cooldown']
        self.animation_max = data['animation_max']

    def Update(self, delta_time):
        if not self.render:
            return False
        self.Update_Damage_Cooldown(delta_time)
        if not self.Update_Cooldown(delta_time):
            return False
        self.Update_Trapped_Entities()
        return True

    def Add_Entity(self, entity):
        # 1. Early exit: Ignore items
        if entity.category == keys.item:
            return False
    
        # 2. Early exit: Already tracked (O(1) dictionary lookup)
        if entity.ID in self.entities:
            return False
        
        # 3. Early exit: Geometric check (call rect() once and cache it)
        if not self.rect().colliderect(entity.rect()):
            return False
        
        # Add to trap tracking
        self.entities[entity.ID] = entity
        return True

    def Remove_Entity(self, entity_ID):
        return self.entities.pop(entity_ID, None) is not None

    def Update_Cooldown(self, delta_time):
        if self.entity_check_cooldown > 0:
            self.entity_check_cooldown -= delta_time
            return False

        self.entity_check_cooldown = COOLDOWN_MAX
        return True
    
    # Handle cooldown of entities in the trap seperately to ensure fast trigger on trap
    # but controlled damage
    def Update_Damage_Cooldown(self, delta_time):
        to_remove = []
        for entity_id  in self.damaged_entities:
            self.damaged_entities[entity_id] -= delta_time
            if self.damaged_entities[entity_id] <= 0:
                to_remove.append(entity_id)

        for entity_id in to_remove:
            self.damaged_entities.pop(entity_id)

    
    def Update_Trapped_Entities(self):
        for entity in self.entities.values():
            if not entity.touching_ground:
                continue
            if entity.ID in self.damaged_entities: # Check if enemy is in damage cooldown
                continue
            if entity.ID == self.ID:
                continue
            
            if not self.rect().colliderect(entity.rect()):
                continue
            self.Apply_Entity_Effect(entity)
            self.damaged_entities[entity.ID] = DAMAGE_COOLDOWN
    
    def Apply_Entity_Effect(self, entity):
        pass

    def Animation_Update(self, delta_time):
        pass


    def Set_Active(self, duration):
        self.active = duration

    def Reduce_Active(self):
        self.active -= 1

