from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# 
class Electric(Effect):
    def __init__(self, entity):
        description = 'Damage and snare,\nspreads to nearby\nenemy, increased\nby wet'
        super().__init__(entity, keys.electric, 5, 0.2, (1, 1.5), description)
        self.snare_time = 1

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.entity.effects.electric_resistance.effect:
            return False
        
        if self.entity.effects.wet.effect:
            effect_time *= 2

        self.entity.Damage_Taken(effect_time, (self.effect_type, 0))
        
        return super().Set_Effect(effect_time, permanent)
    
    def Update_Effect(self, delta_time):

        if self.entity.effects.electric_resistance.effect:
            self.Remove_Effect()
            return False
        



        self.Effect_Animation_Cooldown(delta_time)
        if self.snare_time > 0:
            self.entity.frame_movement = (0, 0)
            self.snare_time -= delta_time
    

        return super().Update_Effect(delta_time)
 

   
    