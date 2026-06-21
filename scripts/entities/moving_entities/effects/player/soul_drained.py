from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Healing disabled until soul recovered
class Soul_Drained(Effect):
    def __init__(self, entity):
        description = 'Healing disabled\nuntil soul recovered'
        super().__init__(entity, keys.soul_drained, 0, 0, (2, 3), description)

    def Update_Effect(self, delta_time):
        if not self.effect_strength:
            return False
        
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