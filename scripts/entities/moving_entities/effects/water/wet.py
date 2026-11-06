from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect
@register_effect(keys.wet)

# Increased damage to electricity but immune to fire
class Wet(Effect):
    def __init__(self, entity):
        description = 'Increases electric\nand prevents fire'
        super().__init__(entity, "wet", 2, 0.3, (3, 4), description)

    
    def Set_Effect(self, effect_time, permanent = False):
        fire_effect = self.Get_Entity_Effect(keys.fire)
        if fire_effect.effect_strength:
            self.Decrease_Other_Effect(keys.fire, fire_effect.effect_strength)

        if self.Get_Entity_Effect_Strength(keys.frozen):
            self.Decrease_Other_Effect(keys.frozen, self.effect_strength)
            
        return super().Set_Effect(effect_time, permanent)

    
    def Update_Effect(self, delta_time):
        # 1. First, check if the effect is still active
        if not self.effect_strength:
            return False
        
        # 2. Logic to suppress fire
        fire_effect = self.Get_Entity_Effect(keys.fire)
        if fire_effect and fire_effect.effect_strength:
            self.Decrease_Other_Effect(keys.fire, fire_effect.effect_strength)
            
        # 3. Update internal timers
        self.Update_Cooldown(delta_time)
        self.Effect_Animation_Cooldown(delta_time)
        
        return True