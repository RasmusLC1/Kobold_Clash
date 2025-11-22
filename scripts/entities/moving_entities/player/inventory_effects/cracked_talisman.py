from scripts.entities.moving_entities.player.inventory_effects.inventory_effect import Inventory_Effect
from scripts.engine.keys.keys import keys

class Cracked_Talisman(Inventory_Effect):
    def __init__(self, entity):
        super().__init__(entity, "cracked_talisman")

    def Set_Decription(self):
        self.description = 'Resistance to\nelemental damage,\n weakness to\nphysical damage'