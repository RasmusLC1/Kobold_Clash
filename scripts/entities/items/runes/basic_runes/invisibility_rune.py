from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Invisibility_Rune(Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.invisibility_rune, pos, amount, rarity_value)

