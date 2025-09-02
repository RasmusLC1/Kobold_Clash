from scripts.entities.moving_entities.effects.effect import Effect
import random
from scripts.engine.keys.keys import keys

# Low damage and slowdown of entity
class Frozen(Effect):
    def __init__(self, entity):
        description = 'Slows and damages\nover time'
        super().__init__(entity, keys.frozen, 2, 0.3, (2, 3), description)

    
    def Set_Effect(self, effect_time, permanent = False):
        if self.entity.effects.fire.effect or self.entity.effects.frozen_resistance.effect:
            return False
        
        if self.entity.effects.wet.effect:
            effect_time *= 2
            self.wet = 0


        return super().Set_Effect(effect_time, permanent)
    
    def Update_Effect(self, delta_time):
        if not self.effect:
            return False
        

        if self.entity.effects.frozen_resistance.effect:
            self.Remove_Effect()
            return False
        
        if self.Update_Cooldown(delta_time):
            damage = random.randint(1, 2)
            self.entity.Damage_Taken(damage, (self.effect_type, 0))
        
        try:
            self.entity.max_speed = max(0.1, self.entity.max_speed / max( 1.1, self.effect // 2))
        except ZeroDivisionError as e:
            print(f"SLOWDOWN: {e}", self.entity.max_speed, self.effect)
        

        self.Effect_Animation_Cooldown(delta_time)

        return True
    