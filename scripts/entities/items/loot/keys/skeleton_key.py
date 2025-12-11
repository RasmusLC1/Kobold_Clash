from scripts.entities.items.loot.keys.key import Key
from scripts.engine.keys.keys import keys


class Skeleton_Key(Key):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.skeleton_key, pos, rarity_value, amount, 5)
        self.radius = 50


    def Set_Description(self):
        self.description = 'Opens door\nquitely'

    def Open_Door(self):
        self.Decrease_Amount(1)
        self.game.clatter.Disable_Clatter()
        if self.amount > 0: # If more than 1 exists return true
            return True
        self.game.inventory.Remove_Item(self)
        self.game.item_handler.Remove_Item(self, True)
        return True
    
