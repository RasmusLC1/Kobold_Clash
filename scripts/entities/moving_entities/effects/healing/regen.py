from scripts.entities.moving_entities.effects.effect import Effect
import random
from scripts.engine.keys.keys import keys

# Regen health over time each time effect is triggered
class Regen(Effect):
    def __init__(self, entity):
        description = 'Heals over time.\nBlocked by poison'
        super().__init__(entity, keys.regen, 5, 30, (80, 100), description)
        self.cooldown = 0
    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if not self.entity.healing_enabled:
            return False
        
        return super().Set_Effect(effect_time, permanent)

    def Update_Regen_Cooldown(self):
        if self.cooldown:
            self.cooldown -= 1
            return False
        
        self.cooldown = 200
        return True
    
    def Update_Cooldown(self):
        state = super().Update_Cooldown()

        if state:
            self.Heal_Entity()
        
        return state

    def Heal_Entity(self):
        self.entity.effects.Set_Effect(keys.healing, random.randint(3, 5))
        self.Effect_Animation_Cooldown()


    def Update_Effect(self):
        if not super().Update_Effect():
            return False
                  
        if self.entity.effects.poison.effect:
            return False
        
        if not self.Update_Regen_Cooldown():
            return False
        
        if random.randint(0, 10) > self.effect:
            return False
        
        self.Heal_Entity()
        return True
