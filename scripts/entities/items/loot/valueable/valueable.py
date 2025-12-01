from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys

class Valuable(Loot):
    def __init__(self, game, type, pos, value, amount = 1, max_amount = 1):
        super().__init__(game, type, pos, (16, 16), value, keys.valuable, amount, max_amount)
        

