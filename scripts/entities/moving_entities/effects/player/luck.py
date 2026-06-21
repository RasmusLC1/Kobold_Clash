from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Reduce the cost runes
class Luck(Effect):
    def __init__(self, entity):
        description = 'You feel lucky'
        super().__init__(entity, keys.luck, 0, 0, (3, 4), description)
        self.effect_max = 10


    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        self.entity.Update_Luck(self.effect_strength) # Set the player's luck to the effect value
        return True
