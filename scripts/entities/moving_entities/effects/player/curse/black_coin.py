from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Increases luck, but increases damage taken
class Black_Coin(Effect):
    def __init__(self, entity):
        description = 'Increases luck\nand damage taken'
        super().__init__(entity, keys.black_coin, 0, 0, (2, 3), description)

    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        self.entity.Update_Luck(self.effect_strength * 2) # Set the player's luck to the effect value * 2
        return True


    def Damage_Taken(self, damage, attacker):
        # Scale: Level 1 = +5% damage, Level 10 = +50% damage
        scaling_factor = 1 + (self.effect_strength * 0.05)
        total_damage = round(damage * scaling_factor)
        
        self.entity.Set_Health(self.entity.health - total_damage)