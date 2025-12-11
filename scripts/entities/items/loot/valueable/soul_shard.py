from scripts.entities.items.loot.valueable.valueable import Valuable
import random
from scripts.engine.keys.keys import keys

class Soul_Shard(Valuable):
    def __init__(self, game, pos):
        super().__init__(game, keys.soul_shard, pos, 1)

    def Pick_Up(self):
        self.game.item_handler.Remove_Item(self, True)
        self.game.player.Remove_Effect(keys.soul_drained, 1)
        return False

    def Set_Description(self):
        self.description = f"Piece of your soul"
