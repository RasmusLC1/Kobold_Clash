from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Eldritch_Mirror(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, "eldritch_mirror")

    def Enable(self):
        pass

    def Disable(self):
        pass
    
    def Set_Decription(self):
        self.description = 'Reflects damage/nworsens negative effects'