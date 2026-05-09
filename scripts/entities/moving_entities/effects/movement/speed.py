from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Increase entity speed
class Speed(Effect):
    def __init__(self, entity):
        description = 'Increases speed'
        super().__init__(entity, keys.speed, 0, 0, (2, 3), description)

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.entity.effects.frozen.effect:
            return False
        return super().Set_Effect(effect_time, permanent)

    def Update_Effect(self, delta_time):

        if not self.effect or self.entity.effects.frozen.effect:
            return False

        self.entity.max_speed = min(4000, self.entity.max_speed * self.effect)
        
        self.Update_Cooldown(delta_time)

        return True