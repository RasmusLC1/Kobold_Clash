from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Muffled_Boots(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, "muffled_boots")

    def Enable(self):
        self.player.Set_Effect(keys.silence, 2, True)


    def Disable(self):
        self.player.Remove_Effect(keys.silence, 2)
    
    def Set_Decription(self):
        self.description = 'reduces noise'