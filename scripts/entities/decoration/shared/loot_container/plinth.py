from scripts.entities.decoration.shared.loot_container.display_loot_container import Display_Loot_Container
from scripts.engine.keys.keys import keys
import random

class Plinth(Display_Loot_Container):
    def __init__(self, game, pos):
        super().__init__(game, keys.plinth, pos, (32, 32), True, 60, 'plinth_shatter', 700)
        
        

    def Drop_Loot(self):
        self.game.item_handler.Spawn_Rune((self.pos[0] + 3, self.pos[1]))

