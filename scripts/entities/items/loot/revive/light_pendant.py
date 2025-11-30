from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys


class Light_Pendant(Loot):
    def __init__(self, game, type, pos, amount, rarity_value):
        self.revive_cost_adjustment = amount
        super().__init__(game, type, pos, size=(16, 16), rarity_value=rarity_value, loot_type=keys.revive, amount=amount)
        

    def Set_Description(self):
        self.description = f"Revive for\n{self.Calculate_Revive_Cost()} {keys.souls}"

    def Calculate_Revive_Cost(self):
            # Divide max health by the adjustment value.
            revive_cost = max(10, self.game.player.max_health / self.revive_cost_adjustment )
            
            return int(revive_cost)

    # Revive the player and scale the cost with the player's max health, then
    # restore health equal to revive cost
    def Revive(self):
        player = self.game.player
        revive_cost =  self.Calculate_Revive_Cost()
        if not player.Decrease_Souls(revive_cost):
            return False

        self.game.particle_handler.Activate_Particles(20, keys.gold_particle, player.rect().center)
        player.Set_Health(revive_cost) # Cheaper revive with higher amount, but less health regained

        player.damage_cooldown = 5
        
        return True
    
        