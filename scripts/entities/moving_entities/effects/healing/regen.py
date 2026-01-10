from scripts.entities.moving_entities.effects.effect import Effect
import random
from scripts.engine.keys.keys import keys

# Regen health over time each time effect is triggered
class Regen(Effect):
    def __init__(self, entity):
        description = 'Heals over time.\nBlocked by poison'
        super().__init__(entity, keys.regen, 5, 0.4, (1.4, 1.8), description)
    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if not self.entity.healing_enabled:
            return False
        
        return super().Set_Effect(effect_time, permanent)

    

    def Heal_Entity(self, delta_time):
        self.entity.effects.Set_Effect(keys.healing, random.randint(3, 5))
        self.Effect_Animation_Cooldown(delta_time)


    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
                  
        if self.entity.effects.poison.effect:
            return False
        
        if self.update_trigged:
            self.update_trigged = False
            self.Heal_Entity(delta_time)
        return True
