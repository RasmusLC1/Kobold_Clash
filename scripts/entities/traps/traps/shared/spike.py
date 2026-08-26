from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from .shared_registry import register_trap

import random

@register_trap(keys.spike_trap, 1900.5)
class Spike(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.spike_trap)
        self.animation = random.randint(0, 5)
        self.slow_amount = 1


    def Apply_Entity_Effect(self, entity):
        entity.Damage_Taken(2, (keys.slow, self.slow_amount))
            

    def Animation_Update(self, delta_time):
        print("TESTETS")
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
            return
        
        if self.animation >= 5:
            self.animation = 0
        else:
            self.animation_handler.Increase_Frame()
        
        self.animation_cooldown = random.uniform(0.3, 0.4)