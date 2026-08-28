from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.frozen_resistance)
# Resistance to freeze
class Frozen_Resistance(Effect):
    def __init__(self, entity):
        description = 'Prevents freezing'
        super().__init__(entity, keys.frozen_resistance, 0, 0, (3, 4), description)

    