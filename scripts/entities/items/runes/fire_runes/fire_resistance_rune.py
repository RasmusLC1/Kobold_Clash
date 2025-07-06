from scripts.entities.items.runes.rune import Rune

from scripts.engine.keys.keys import keys

class Fire_Resistance_Rune(Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.fire_resistance_rune, pos, 5, 15)
        self.animation_time_max = 20
        self.animation_size_max = 25


        

    