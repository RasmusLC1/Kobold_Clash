from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Vampiric_Rune(Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.vampiric_rune , pos, 4, 25)
