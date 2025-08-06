from scripts.entities.items.loot.valueable.valueable import Valuable
import random
from scripts.engine.keys.keys import keys

class Soul_Shard(Valuable):
    def __init__(self, game, pos):
        super().__init__(game, keys.soul_shard, pos, 1)
        self.description = f"Piece of your soul"

    def Pick_Up(self):
        self.game.player.Set_Effect(keys.soul_drained, 1, True)
        self.game.item_handler.Remove_Item(self, True)
        return False