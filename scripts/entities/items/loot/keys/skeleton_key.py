from scripts.entities.items.loot.keys.key import Key
from scripts.engine.keys.keys import keys


class Skeleton_Key(Key):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.skeleton_key, pos, rarity_value)
        self.radius = 50

    def Set_Description(self):
        self.description = 'Opens door\nquitely 1 time'

    def Open_Door(self):
        self.game.inventory.Remove_Item(self)
        self.game.item_handler.Remove_Item(self, True)
        self.game.clatter.Disable_Clatter()
        return True
    
