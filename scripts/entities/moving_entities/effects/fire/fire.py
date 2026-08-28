from scripts.entities.moving_entities.effects.effect import Effect
import random
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.fire)
# Take fire damage
class Fire(Effect):
    def __init__(self, entity):
        description = 'fire Damage over time.\nStopped by water\nIncreases damage\ntaken'
        super().__init__(entity, keys.fire, 7, 0.3, (0.5, 1), description)

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.Get_Entity_Effect_Strength(keys.wet) or self.Get_Entity_Effect_Strength(keys.fire_resistance):
            return False
        frozen_effect = self.entity.Get_Effect(keys.frozen)
        if frozen_effect:
            frozen_effect.Remove_Effect()
            
        return super().Set_Effect(effect_time, permanent)
    
    def Update_Effect(self, delta_time):
        if not self.effect_strength:
            return False
        
        if self.Check_Resistance():
            return False
        
        if self.Update_Cooldown(delta_time):
            damage = random.randint(2, 3)
            self.entity.Damage_Taken(damage, (self.effect_type, 0))


        self.Effect_Animation_Cooldown(delta_time)
        return True
    
    def Check_Resistance(self):
         # Check for resistances
        wet_effect = self.entity.Get_Effect(keys.wet)
        if self.Get_Entity_Effect_Strength(keys.fire_resistance) or wet_effect.effect_strength:
            self.effect_strength = 0
            self.cooldown = 0
            if wet_effect:
                wet_effect.Decrease_Effect()
            return True
        
        return False
    
    # Takes up to 50% additional damage
    def Damage_Taken(self, damage, attacker):
        # Scale the bonus damage: lower damage gets closer to a 1.5x multiplier.
        scaling_factor = (10 - self.effect_strength) / 10  
        bonus_percent = max(0.0, min(0.5, scaling_factor * 0.5))
        damage_multiplier = 1.0 + bonus_percent
        
        final_damage = max(1, int(damage * damage_multiplier))
        
        # Set health directly to avoid infinite damage loop
        self.entity.Set_Health(self.entity.health - final_damage) 