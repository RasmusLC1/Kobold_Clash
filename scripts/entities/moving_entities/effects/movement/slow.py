from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.slow)
# Reduce the entity speed
class Slow(Effect):
    def __init__(self, entity):
        description = 'Reduces speed'
        super().__init__(entity, keys.slow, 0, 0, (1, 1.3), description)

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        return super().Set_Effect(effect_time, permanent)

    def Update_Effect(self, delta_time):

        if not self.effect_strength:
            return False

        try:
            self.entity.max_speed = max(0.1, self.entity.max_speed / self.effect_strength)
        except ZeroDivisionError as e:
            print(f"SLOWDOWN: {e}", self.entity.max_speed, self.effect_strength)
        self.Update_Cooldown(delta_time)

        return True
    
