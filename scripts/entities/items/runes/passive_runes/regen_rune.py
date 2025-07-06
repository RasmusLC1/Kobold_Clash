from scripts.entities.items.runes.passive_runes.passive_rune import Passive_Rune
from scripts.engine.keys.keys import keys


class Regen_Rune(Passive_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.regen_rune, pos, 2, 1000, 30)

    