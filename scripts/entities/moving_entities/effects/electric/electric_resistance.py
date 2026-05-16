from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Reduce fire damage
class Electric_Resistance(Effect):
    def __init__(self, entity):
        description = 'Prevents electric'
        super().__init__(entity, keys.electric_resistance, 0, 0, (3, 4), description)

