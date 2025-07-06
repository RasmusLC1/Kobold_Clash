from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Anchor_Stone(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, "anchor_stone")

    def Enable(self):
        self.player.Set_Effect('anchor', 1, True)
        

    def Disable(self):
        self.player.Remove_Effect('anchor', 1)
        
    
    def Set_Decription(self):
        self.description = 'Prevents pushing'