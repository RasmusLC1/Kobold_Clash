from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Faith_Pendant(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, "faith_pendant")


    def Set_Decription(self):
        self.description = 'highlights traps'