from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from .shared_registry import register_trap
import random

CLATTER_RANGE = 500
@register_trap(keys.rubble, 1)
class Rubble(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.rubble)
        self.animation = random.randint(0, 3)


    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return
        
        self.Generate_Sound(keys.rubble, 0.4, CLATTER_RANGE)

