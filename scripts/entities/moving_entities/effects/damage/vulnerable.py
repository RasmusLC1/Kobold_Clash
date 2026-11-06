from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.vulnerable)
# Take extra damage
class Vulnerable(Effect):
    def __init__(self, entity):
        description = 'Increases damage\ntaken'
        super().__init__(entity, 'vulnerable', 0, 0, (2, 3), description)

    
    def Damage_Taken(self, damage, attacker):
        self.entity.Set_Health(self.entity.health - damage // 2)