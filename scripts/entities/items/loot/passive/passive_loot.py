from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys

# Generic passive loot that changes depending on the type, simplified to one
# class since it uses effects
class Passive_Loot(Loot):
    def __init__(self, game, type, pos):
        super().__init__(game, type, pos, (16, 16), 10, keys.passive)

    def Pick_Up(self):
        if not super().Pick_Up():
            return False
        
        self.game.player.inventory_effects.Enable(self.type)
        return True

    def Place_Down(self):
        if not super().Place_Down():
            return False
        
        self.game.player.inventory_effects.Disable(self.type)
        return True

        
