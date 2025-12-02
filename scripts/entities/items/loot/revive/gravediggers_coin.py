from scripts.entities.items.loot.loot import Loot
import random
from scripts.engine.keys.keys import keys

# Revives for gold
class Gravediggers_Coin(Loot):
    def __init__(self, game, type, pos, amount, rarity_value):
        self.gold_cost_to_revive = int(99 // amount)
        print(self.gold_cost_to_revive)
        self.revive_health_amount = int(max(10, game.player.max_health // amount // 2))
        super().__init__(game, type, pos, size=(16, 16), rarity_value=rarity_value, loot_type=keys.revive, amount=amount)

    
    def Set_Description(self):
        self.description = f"Revive for {self.gold_cost_to_revive} {keys.gold}"

    def Revive(self):
        player = self.game.player

        if not player.Pay_Gold(self.gold_cost_to_revive):
            return False
        
        self.game.particle_handler.Activate_Particles(20, keys.gold_particle, player.pos)
        player.Set_Health(self.revive_health_amount)
        player.damage_cooldown = 5
        self.game.item_handler.Remove_Item(self, True)
        self.game.inventory.Remove_Item(self)
        
        return True