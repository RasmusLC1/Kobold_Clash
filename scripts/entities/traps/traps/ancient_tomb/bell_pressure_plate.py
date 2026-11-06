from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from .ancient_tomb_registry import register_trap


CLATTER_RANGE = 1000

@register_trap(keys.bell_pressure_plate, 0.6)
class Bell_Pressure_plate(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.pressure_plate)


    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return
        
        self.Generate_Sound(keys.bell, 0.3, CLATTER_RANGE)
