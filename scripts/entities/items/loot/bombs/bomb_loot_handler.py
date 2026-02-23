from scripts.entities.items.loot.bombs.bomb import Bomb
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler

import random
from scripts.engine.keys.keys import keys


class Bomb_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

        self.loot_map = {
            keys.fire_bomb : Bomb,
            keys.frozen_bomb : Bomb,
            keys.electric_bomb : Bomb,
            keys.poison_bomb : Bomb,
            keys.vampiric_bomb : Bomb,
        }
        self.loot_types_cost = {
            keys.fire_bomb : 15,
            keys.frozen_bomb : 15,
            keys.electric_bomb : 15,
            keys.poison_bomb : 15,
            keys.vampiric_bomb : 20,
        }
