from scripts.entities.items.loot.loot import Loot
import random
from scripts.engine.keys.keys import keys


class Light_Pendant(Loot):
    def __init__(self, game, pos):
        super().__init__(game, keys.phoenix_feather, pos, (16, 16), 10, keys.revive)
        self.description = f"Revive for\n{self.game.player.max_health * 2} soul"


    # Revive the player and scale the cost with the player's max health, then
    # restore half health
    def Revive(self):
        player = self.game.player
        revive_cost =  player.max_health * 2
        if player.Get_Total_Available_Souls() < revive_cost:
            return False
        self.game.particle_handler.Activate_Particles(20, keys.gold_particle, player.rect().center)
        player.Set_Health(player.max_health // 2)
        player.Decrease_Souls(revive_cost)

        player.damage_cooldown = 100
        
        return True
    
        