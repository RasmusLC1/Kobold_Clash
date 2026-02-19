from scripts.entities.items.runes.passive_runes.passive_rune import Passive_Rune
from scripts.engine.keys.keys import keys


class Regen_Rune(Passive_Rune):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.regen_rune, pos, amount, 18, 30, rarity_value)

    