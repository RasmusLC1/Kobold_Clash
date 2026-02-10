from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys

class Invulnerable_Rune(Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.invulnerable_rune, pos, 4, 60)
