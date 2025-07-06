from scripts.entities.moving_entities.effects.effect import Effect
import random
from scripts.engine.keys.keys import keys

# Set entity movement speed to zero
class Snare(Effect):
    def __init__(self, entity):
        description = 'Prevents movement'
        super().__init__(entity, keys.snare, 0, 0, (50, 70), description)

    
    # Set effect so that it picks the highest effect time, but does not stack them
    # to prevent permanent being stuck
    def Set_Effect(self, effect_time, permanent = False):
        self.effect = max(self.effect, min(effect_time, 10))
        return True
    
    def Update_Effect(self):
        if not self.effect:
            return False
        
        if self.cooldown:
            self.cooldown -= 1
        else:
            self.effect -= 1
            self.cooldown = random.randint(50, 70)
        
        self.entity.frame_movement = (0, 0)
        return True
    
    def Push(self, direction):
        self.entity.Set_Frame_movement((0, 0)) # Cancel frame movement