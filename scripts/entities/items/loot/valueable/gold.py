from scripts.entities.items.loot.valueable.valueable import Valuable

import random
from scripts.engine.keys.keys import keys

class Gold(Valuable):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, type, pos, value=1, amount=amount, max_amount = 99, max_animation=3)



    def Set_Description(self):
        self.description = f"gold {self.amount}\n"
