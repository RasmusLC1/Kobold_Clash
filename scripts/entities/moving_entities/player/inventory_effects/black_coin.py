from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Black_Coin(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, keys.black_coin)

    def Set_Decription(self):
        self.description = 'Increases gold\nand damage taken'