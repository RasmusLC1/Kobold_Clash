from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from .shared_registry import register_trap

import random

@register_trap(keys.spike_trap, 0.5)
class Spike(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.spike_trap, max_animation=5, animation_cooldown_max=0.4)
        self.slow_amount = 1


    def Apply_Entity_Effect(self, entity):
        entity.Damage_Taken(2, (keys.slow, self.slow_amount))
            
