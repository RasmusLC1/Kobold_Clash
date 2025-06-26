from scripts.entities.decoration.decoration import Decoration
from scripts.engine.assets.keys import keys

class Weapon_rack(Decoration):
    def __init__(self, game, pos):
        super().__init__(game, keys.weapon_rack, pos, (32, 32), True, 20)


    def Spawn_Weapons(self):
        self.game.item_handler.Spawn_Weapon((self.pos[0], self.pos[1] + 1))
