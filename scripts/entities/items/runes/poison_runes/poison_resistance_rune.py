from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Poison_Resistance_Rune(Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.poison_resistance_rune, pos, amount, rarity_value, animation_time_max = 0.3, animation_size_max = 25)


        

    