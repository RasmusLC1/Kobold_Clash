from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Reduce the cost runes
class Arcane_Conduit(Effect):
    def __init__(self, entity):
        description = 'Reduces Rune cost'
        super().__init__(entity, keys.arcane_conduit, 0, 0, (3, 4), description)

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        self.effect = effect_time
        return True
    
    