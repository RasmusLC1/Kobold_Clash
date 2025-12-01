from scripts.entities.items.loot.valueable.valueable import Valuable

import random
from scripts.engine.keys.keys import keys

class Gold(Valuable):
    def __init__(self, game, pos, amount = 1):
        print(amount)
        super().__init__(game, keys.gold, pos, value=1, amount=amount, max_amount = 99)
        self.animation = random.randint(1, 3)



    def Set_Description(self):
        self.description = f"gold {self.amount}\n"
