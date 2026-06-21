from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Power effect is added to the rune's power in the rune itself
class Power(Effect):
    def __init__(self, entity):
        description = 'Increases Rune power'
        super().__init__(entity, keys.power, 0, 0, (2, 3), description)

    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        
        
        self.entity.Update_Rune_Power(self.effect_strength) # Set the player's rune power to the effect value

        if  self.update_trigged:
            self.entity.game.inventory.rune_inventory.Set_Descriptions()

        return True
    
