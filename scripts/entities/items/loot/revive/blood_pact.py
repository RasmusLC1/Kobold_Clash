from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys
from  scripts.entities.items.loot.curse.effect_curse import Effect_Curse


class Blood_Pact(Loot):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, type, pos, size=(16, 16), rarity_value=rarity_value, loot_type=keys.revive, amount=amount)
        self.curse_intensity = max(1, 4 - amount)
        self.revive_health_amount = int(max(10, self.game.player.max_health // amount))

    
    def Set_Description(self):
        self.description = f"Protected against death\nBut at what cost"

    def Revive(self):
        player = self.game.player

        curse = Effect_Curse.Set_Random_Negative_Effect()
        self.entity.Set_Effect(curse, self.curse_intensity, True)

        self.game.particle_handler.Activate_Particles(20, keys.vampire_particle, player.pos)
        player.Set_Health(self.revive_health_amount)
        player.damage_cooldown = 5
        self.game.item_handler.Remove_Item(self, True)
        self.game.inventory.Remove_Item(self)
        
        return True