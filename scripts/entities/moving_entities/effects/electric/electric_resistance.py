from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Reduce fire damage
class Electric_Resistance(Effect):
    def __init__(self, entity):
        description = 'Prevents electric'
        super().__init__(entity, keys.electric_resistance, 0, 0, (200, 250), description)

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.effect >= self.effect_max:
            return False
        
        return super().Set_Effect(effect_time, permanent)
