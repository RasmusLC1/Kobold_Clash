from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Silence_Rune(Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.silence_rune, pos, 3, 40)