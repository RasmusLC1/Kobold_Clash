from scripts.entities.items.loot.loot import Loot
import random
from scripts.engine.keys.keys import keys

# Revives the player for free, but with very little health
class Phoenix_Feather(Loot):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, type, pos, size=(16, 16), rarity_value=rarity_value, loot_type=keys.revive, amount=amount)
        self.health_on_revive = 10 * amount

    
    def Set_Description(self):
        self.description = f"Revive with {self.health_on_revive} {keys.health}"

    def Revive(self):
        self.game.particle_handler.Activate_Particles(20, keys.gold, self.game.player.pos)
        self.game.player.Set_Health(self.health_on_revive)
        self.game.player.damage_cooldown = 5
        self.game.item_handler.Remove_Item(self, True)
        self.game.inventory.Remove_Item(self)
        
        return True