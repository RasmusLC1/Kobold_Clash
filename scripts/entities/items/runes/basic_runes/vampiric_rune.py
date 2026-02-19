from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Vampiric_Rune(Rune):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.vampiric_rune , pos, amount, rarity_value)
