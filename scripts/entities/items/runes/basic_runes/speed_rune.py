from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys

class Speed_Rune(Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.speed_rune, pos, 3, 25)
        self.animation_time_max = 0.5
        self.animation_size_max = 15
