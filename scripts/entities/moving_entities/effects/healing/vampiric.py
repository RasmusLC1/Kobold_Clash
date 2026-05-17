from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Heal entity when dealing damage
class Vampiric(Effect):
    def __init__(self, entity):
        description = 'Heals when\ndealing damage'
        super().__init__(entity, keys.vampiric, 0, 0, (3, 4), description)


    def Damage_Dealt(self, damage):
        modifier = 10 - self.effect_strength
        damage_heal = max(1, damage // modifier)
        self.entity.Set_Effect(keys.healing, damage_heal)