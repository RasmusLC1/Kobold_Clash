from scripts.entities.items.loot.keys.key import Key
import random
from scripts.engine.keys.keys import keys

class Lockpick(Key):
    def __init__(self, game, pos):
        super().__init__(game, keys.lockpick, pos)
        self.description = '1/3 chance\nto persist'
        self.amount = 1
        self.max_amount = 3

    def Open_Door(self):
        # If item persist no further action done
        if random.randint(1, 3) != 1:
            return True
        game = self.game # cache game for quick lookup
        game.inventory.Remove_Item(self)
        game.item_handler.Remove_Item(self, True)
        game.clatter.Generate_Clatter(self.pos, 1000) # Generate extra clatter for failure
        return True