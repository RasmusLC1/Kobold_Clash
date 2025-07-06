from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Increased damage to electricity but immune to fire
class Wet(Effect):
    def __init__(self, entity):
        description = 'Increases electric\nand prevents fire'
        super().__init__(entity, "wet", 2, 20, (200, 250), description)

    
    def Set_Effect(self, effect_time, permanent = False):
        if self.entity.effects.fire.effect:
            self.effects.fire.Remove_Effect()

        if self.entity.effects.frozen:
            self.entity.effects.frozen.Decrease_Effect()
            
        return super().Set_Effect(effect_time, permanent)

    
    def Update_Effect(self):
        if not self.effect:
            return False
        
        if self.entity.effects.fire.effect:
            self.entity.effects.fire.Remove_Effect()
            
        self.Update_Cooldown()
        
        self.Effect_Animation_Cooldown()
        return False
    