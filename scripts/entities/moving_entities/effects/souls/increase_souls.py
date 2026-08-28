from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.increase_souls)
# Increase player souls once
class Increase_Souls(Effect):
    def __init__(self, entity):
        description = 'Increase Souls once'
        super().__init__(entity, keys.increase_souls, 0, 0, (0,0), description)

    
    def Set_Effect(self, effect_time, permanent = False):
        if self.entity.type != 'player':
            return False
        self.entity.Increase_Souls(effect_time)
        return True
