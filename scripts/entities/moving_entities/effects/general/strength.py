from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.strength)
# Increase entity's strength
class Increase_Strength(Effect):
    def __init__(self, entity):
        description = 'Increases\nmelee damage'
        super().__init__(entity, keys.increase_strength, 0, 0, (2, 3), description)
    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.Get_Entity_Effect_Strength(keys.poison):
            return False
        return super().Set_Effect(effect_time, permanent)


    def Update_Effect(self, delta_time):
        if not self.effect_strength or self.Get_Entity_Effect_Strength(keys.poison):
            return False
        self.entity.strength = min(20, self.entity.strength + self.effect_strength)

        self.Update_Cooldown(delta_time)

        return True


