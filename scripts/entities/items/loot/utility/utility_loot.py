from scripts.entities.items.loot.interactive_loot import Interactive_Loot
from scripts.engine.keys.keys import keys

class Utility_Loot(Interactive_Loot):
    def __init__(self, game, type, pos, max_distance, amount, value, max_amount = 5):
        super().__init__(game, type, pos, max_distance, (16, 16), keys.utility,
                         value, amount, max_amount = max_amount)