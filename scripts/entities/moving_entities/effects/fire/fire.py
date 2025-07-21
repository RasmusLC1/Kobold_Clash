from scripts.entities.moving_entities.effects.effect import Effect
import random
from scripts.engine.keys.keys import keys

# Take fire damage
class Fire(Effect):
    def __init__(self, entity):
        description = 'fire Damage over time.\nStopped by water\nIncreases damage\ntaken'
        super().__init__(entity, keys.fire, 7, 0.3, (0.5, 1), description)

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.entity.effects.wet.effect or self.entity.effects.fire_resistance.effect:
            return False
        if self.entity.effects.frozen.effect:
            self.entity.effects.frozen.Remove_Effect()
            
        return super().Set_Effect(effect_time, permanent)
    
    def Update_Effect(self, delta_time):
        if not self.effect:
            return False
        
        # Check for resistances
        if self.entity.effects.fire_resistance.effect or self.entity.effects.wet.effect:
            self.effect = 0
            self.cooldown = 0
            if self.entity.effects.wet.effect:
                self.entity.effects.wet.Decrease_Effect()
            return False
        
        if self.Update_Cooldown(delta_time):
            damage = random.randint(2, 3)
            self.entity.Damage_Taken(damage, (self.effect_type, 0))


        self.Effect_Animation_Cooldown(delta_time)
        return True
    
    def Damage_Taken(self, damage):
        self.entity.Set_Health(self.entity.health - max(1, damage // 2))