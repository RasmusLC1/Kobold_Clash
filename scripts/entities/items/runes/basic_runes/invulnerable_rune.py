from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys

class Invulnerable_Rune(Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.invulnerable_rune, pos, 4, 60)
        self.animation_time_max = 0.5
        self.animation_size_max = 15

