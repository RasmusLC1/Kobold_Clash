from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Strength_Totem(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, "strength_totem")
        self.strength = 4

    def Enable(self):
        self.player.Set_Effect('increase_strength', self.strength, True)
        

    def Disable(self):
        self.player.Remove_Effect('increase_strength', self.strength)
    
    def Set_Decription(self):
        self.description = 'Increases strength by 4'