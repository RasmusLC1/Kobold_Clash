from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Take extra damage
class Vulnerable(Effect):
    def __init__(self, entity):
        description = 'Increases damage\ntaken'
        super().__init__(entity, 'vulnerable', 0, 0, (100, 150), description)

    
    def Damage_Taken(self, damage):
        self.entity.Set_Health(self.entity.health - damage // 2)