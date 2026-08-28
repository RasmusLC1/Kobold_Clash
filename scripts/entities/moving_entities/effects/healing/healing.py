from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.healing)
# Heal entity
class Healing(Effect):
    def __init__(self, entity):
        description = 'One time healing.\nBlocked by poison'
        super().__init__(entity, keys.healing, 0, 0, (0,0), description)

    
    def Set_Effect(self, effect_time, permanent = False):
        if not self.entity.healing_enabled:
            return False
        
        if self.entity.health >= self.entity.max_health:
            return False    
        self.entity.Update_Health(effect_time)
        return True
