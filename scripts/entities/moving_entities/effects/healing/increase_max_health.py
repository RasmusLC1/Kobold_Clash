from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.increase_max_health)
# Heal entity
class Increase_Max_Health(Effect):
    def __init__(self, entity):
        description = ''
        super().__init__(entity, keys.increase_max_health, 0, 0, (0,0), description)

    
    def Set_Effect(self, effect_time, permanent = False):
        
        self.entity.Increase_Max_Health(effect_time)
        return True
