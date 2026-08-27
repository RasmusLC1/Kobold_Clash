from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from .shared_registry import register_trap
import random


@register_trap(keys.spike_poison_trap, 0.4)
class Spike_Poisoned(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.spike_poison_trap, max_animation=13, animation_cooldown_max=0.2)
        
    def Apply_Entity_Effect(self, entity):
        entity.Damage_Taken(2, (keys.poison, random.randint(3,5)))


 
