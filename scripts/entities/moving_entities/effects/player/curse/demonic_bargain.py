from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Scales damage but prevent healing
class Demonic_Bargain(Effect):
    def __init__(self, entity):
        description = 'Doubles strength,\nprevents healing'
        super().__init__(entity, keys.demonic_bargain, 0, 0, (2, 3), description)

    def Update_Effect(self, delta_time):
        if not self.effect_strength:
            return False
        
        if self.entity.Get_Effect_Strength(keys.poison):
            return True
        
        self.entity.strength = min(20, self.entity.strength * self.effect_strength)

        self.Update_Cooldown(delta_time)
        return True


    # If effect is sucessful disable healing
    def Set_Effect(self, effect_time, permanent = False):
        if not super().Set_Effect(effect_time, permanent):
            return False
        
        self.entity.Set_Healing_Enabled(False)
        return True

    
    def Remove_Effect(self, reduce_permanent=0):
        if not super().Remove_Effect(reduce_permanent):
            return False
        
        self.entity.Set_Healing_Enabled(True)
        return True