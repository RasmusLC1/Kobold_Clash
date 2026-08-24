from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys


CLATTER_RANGE = 1000

class Bell_Pressure_plate(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.pressure_plate)


    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return
        
        self.Generate_Sound(keys.bell, 0.3, CLATTER_RANGE)
