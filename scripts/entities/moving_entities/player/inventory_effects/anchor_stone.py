from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Anchor_Stone(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, keys.anchor)

    
    def Set_Decription(self):
        self.description = 'Prevents pushing'