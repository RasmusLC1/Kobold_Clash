from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Silence_Rune(Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.silence_rune, pos, 3, 40)
        self.animation_time_max = 30
        self.animation_size_max = 15

