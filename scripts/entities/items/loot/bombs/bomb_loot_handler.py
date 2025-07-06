from scripts.entities.items.loot.bombs.bomb import Bomb
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler

import random
from scripts.engine.keys.keys import keys


class Bomb_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)
 

        self.types = [
            keys.fire_bomb,
            keys.frozen_bomb,
            keys.electric_bomb,
            keys.poison_bomb,
            keys.vampiric_bomb,
        ]

    def Loot_Spawner(self, pos, type = None, amount = None):
        if not type:
            type = random.choice(self.types)
        bomb = Bomb(self.game, type, pos)
        return bomb

