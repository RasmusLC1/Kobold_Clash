from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys

class Valuable(Loot):
    def __init__(self, game, type, pos, value, amount = 1, max_amount = 1,
                 max_animation=0, animation_cooldown_max = 0):
        super().__init__(game, type, pos, (16, 16), value, keys.valuable,
                         amount, max_amount, max_animation=max_animation,
                         animation_cooldown_max=animation_cooldown_max)
        

