from scripts.entities.moving_entities.effects.effect import Effect
import random
from scripts.engine.keys.keys import keys

# Set entity movement speed to zero
class Snare(Effect):
    def __init__(self, entity):
        description = 'Prevents movement'
        super().__init__(entity, keys.snare, 0, 0, (1, 1.2), description)

    
    # Set effect so that it picks the highest effect time, but does not stack them
    # to prevent permanent being stuck
    def Set_Effect(self, effect_time, permanent = False):
        self.effect_strength = max(self.effect_strength, min(effect_time, 10))
        return True
    
    def Update_Effect(self, delta_time):
        if not self.effect_strength:
            return False
        
        self.Update_Cooldown(delta_time)
        
        self.entity.frame_movement = (0, 0)
        return True
    
    def Push(self, direction):
        self.entity.Set_Frame_movement((0, 0)) # Cancel frame movement