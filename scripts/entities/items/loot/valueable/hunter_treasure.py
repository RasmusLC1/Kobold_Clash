from scripts.entities.items.loot.valueable.valueable import Valuable
import random
from scripts.engine.keys.keys import keys

class Hunter_Treasure(Valuable):
    def __init__(self, game, pos):
        super().__init__(game, keys.hunter_treasure, pos, 1)
        self.description = f"Return to\nhunter shrine"
