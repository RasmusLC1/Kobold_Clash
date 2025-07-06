from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Don't generate sound and clatter
class Blood_Tomb(Effect):
    def __init__(self, entity):
        description = 'Gain souls\nwhen damaged'
        super().__init__(entity, keys.blood_tomb, 0, 0, (120, 160), description)


    def Damage_Taken(self, damage):
        self.entity.Increase_Souls(damage * self.effect * 2)