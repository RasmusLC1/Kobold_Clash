from scripts.entities.items.loot.loot import Loot
import random
from scripts.engine.keys.keys import keys


class Phoenix_Feather(Loot):
    def __init__(self, game, pos):
        super().__init__(game, keys.phoenix_feather, pos, (16, 16), 10, keys.revive)

    def Revive(self):
        self.game.particle_handler.Activate_Particles(20, keys.gold, self.game.player.pos, frame=random.randint(40, 60))
        self.game.player.Set_Health(1)
        self.game.player.damage_cooldown = 500
        self.game.item_handler.Remove_Item(self, True)
        self.game.inventory.Remove_Item(self)
        
        return True