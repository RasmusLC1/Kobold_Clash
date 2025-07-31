from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Resistance_Rune(Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.resistance_rune, pos, 3, 15)
        self.animation_time_max = 0.5
        self.animation_size_max = 15
        self.clicked = False

