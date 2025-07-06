from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Halo(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, keys.halo)

    def Enable(self):
        self.player.Set_Effect(keys.halo, 1, True)
        

    def Disable(self):
        self.player.Remove_Effect(keys.halo, 1)


    def Set_Decription(self):
        self.description = '1/10 chance\nto cancel damage'