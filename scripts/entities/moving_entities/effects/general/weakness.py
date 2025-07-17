from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Increase entity's strength
class Weakness(Effect):
    def __init__(self, entity):
        description = 'Decreases\nmelee damage'

        super().__init__(entity, keys.weakness, 0, 0, (2, 3), description)

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        # Double the effect if poisoned
        if self.entity.effects.poison.effect:
            effect_time *= 2
        return super().Set_Effect(effect_time, permanent)


    def Update_Effect(self, delta_time):

        if not self.effect:
            return False
        
        self.entity.strength = min(20, self.entity.strength // 2)

        self.Update_Cooldown(delta_time)

        return True
    