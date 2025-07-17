from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Increases gold, but increases damage taken
class Black_Coin(Effect):
    def __init__(self, entity):
        description = 'Increases gold\nand damage\ntaken'
        super().__init__(entity, keys.black_coin, 0, 0, (2, 3), description)


    def Damage_Taken(self, damage):
        self.entity.Set_Health(self.health - damage // 4)