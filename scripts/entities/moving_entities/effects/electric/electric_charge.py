from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.electric_charge)
# If entity is damaged, sets electric effect back to entity that attacked
class Electric_Charge(Effect):
    def __init__(self, entity):
        description = 'Shocks the attacker'
        super().__init__(entity, keys.electric_charge, 0, 0, (3, 4), description)

    # If entity has 10 electric_charge strength, attacking enemy gets 5 electric
    def Damage_Taken(self, damage, attacker):
        if not attacker:
            return
        attacker.Set_Effect(keys.electric, self.effect_strength // 2)