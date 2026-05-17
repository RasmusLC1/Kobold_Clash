from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Return damage dealth to entity
class Thorns(Effect):
    def __init__(self, entity):
        description = 'Reflects damage\nback to\nattackers'
        super().__init__(entity, keys.thorns, 0, 0, (3, 4), description)
        self.type = 'slash'


    def Set_Type(self, type):
        self.type = type

    def Damage_Taken(self, damage, attacker=None):
        if not attacker:
            return
        scaling_factor = (10 - self.effect_strength) / 10  
        bonus_percent = max(0.0, min(0.5, scaling_factor * 0.5))
        damage_multiplier = 1.0 + bonus_percent
        
        final_damage = max(1, int(damage * damage_multiplier))
        attacker.Damage_Taken(final_damage, self.entity.attack_direction)