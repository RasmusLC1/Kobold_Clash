from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Demonic_Bargain(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, keys.demonic_bargain)

    def Enable(self):
        self.player.Set_Effect(keys.demonic_bargain, 1, True)
        

    def Disable(self):
        self.player.Remove_Effect(keys.demonic_bargain, 1)
    
    def Set_Decription(self):
        self.description = 'Increases damage/nPrevents healing'