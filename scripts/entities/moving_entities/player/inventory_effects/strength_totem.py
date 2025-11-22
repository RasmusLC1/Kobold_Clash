from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Strength_Totem(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, keys.strength_totem)
        self.strength = 4

    def Set_Decription(self):
        self.description = 'Increases strength by 4'