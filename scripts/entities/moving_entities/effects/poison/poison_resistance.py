from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.poison_resistance)
# Resist poison
class Poison_Resistance(Effect):
    def __init__(self, entity):
        description = 'Prevents poison'
        super().__init__(entity, keys.poison_resistance, 0, 0, (3, 4), description)

