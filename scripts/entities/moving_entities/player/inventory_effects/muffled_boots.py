from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Muffled_Boots(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, keys.silence)

    
    def Set_Decription(self):
        self.description = 'reduces noise'