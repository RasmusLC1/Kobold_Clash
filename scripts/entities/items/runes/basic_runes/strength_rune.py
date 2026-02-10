from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys

class Strength_Rune(Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.increase_strength_rune , pos, 3, 20)