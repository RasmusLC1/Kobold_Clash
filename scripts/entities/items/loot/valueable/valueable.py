from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys

class Valuable(Loot):
    def __init__(self, game, type, pos, value):
        super().__init__(game, type, pos, (16, 16), value, keys.valuable)
