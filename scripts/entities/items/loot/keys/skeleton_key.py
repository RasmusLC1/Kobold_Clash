from scripts.entities.items.loot.keys.key import Key
from scripts.engine.keys.keys import keys


class Skeleton_Key(Key):
    def __init__(self, game, pos):
        super().__init__(game, keys.skeleton_key, pos)
        self.radius = 50
        self.description = 'Opens door\nquitely'


    def Open_Door(self):
        self.game.inventory.Remove_Item(self)
        self.game.item_handler.Remove_Item(self, True)
        self.game.clatter.Disable_Clatter()
        return True
    
