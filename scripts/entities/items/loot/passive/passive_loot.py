from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys

# Generic passive loot that changes depending on the type, simplified to one
# class since it uses effects
class Passive_Loot(Loot):
    def __init__(self, game, type, pos, effect_power, rarity_value):
        self.effect_power = int(effect_power)
        super().__init__(game, type, pos, (16, 16), rarity_value=rarity_value, loot_type=keys.passive)

    def Pick_Up(self):
        if not super().Pick_Up():
            return False
        
        self.game.player.Enable_Inventory_Effect(self.type, self.effect_power)
        return True

    def Place_Down(self):
        if not super().Place_Down():
            return False
        
        self.game.player.Disable_Inventory_Effect(self.type, self.effect_power)

        return True

        
