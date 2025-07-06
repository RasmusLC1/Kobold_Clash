from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Increase entity's strength
class Increase_Strength(Effect):
    def __init__(self, entity):
        description = 'Increases\nmelee damage'
        super().__init__(entity, "increase_strength", 0, 0, (130, 160), description)
    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.entity.effects.poison.effect:
            return False
        return super().Set_Effect(effect_time, permanent)


    def Update_Effect(self):
        if not self.effect or self.entity.effects.poison.effect:
            return False
        self.entity.strength = min(20, self.entity.strength + self.effect)

        self.Update_Cooldown()

        return True


