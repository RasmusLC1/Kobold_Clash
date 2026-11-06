from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from .shared_registry import register_trap

@register_trap(keys.pit_trap, 0.4)
class Spike_Pit(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.pit_trap)
        self.slow_amount = 1
        

    def Apply_Entity_Effect(self, entity):
        if not self.animation:
            self.animation = 1
            entity.Damage_Taken(10, (keys.snare, 2))
        else:
            entity.Damage_Taken(5, (keys.slow, self.slow_amount))
