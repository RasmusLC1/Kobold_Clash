from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from .shared_registry import register_trap
import random


@register_trap(keys.spike_poison_trap, 0.4)
class Spike_Poisoned(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.spike_poison_trap)
        self.animation = random.randint(0, 13)

        
    def Apply_Entity_Effect(self, entity):
        entity.Damage_Taken(2, (keys.poison, random.randint(3,5)))


    def Animation_Update(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
            return
        
        if self.animation >= 13:
            self.animation = 0
        else:
            self.animation += 1
        
        self.animation_cooldown = random.uniform(0.13, 0.15)
