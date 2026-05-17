from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Improves runes but reduces strength
class Forsaken_Grimoire(Effect):
    def __init__(self, entity):
        description = 'Improves runes\nbut reduces strength'
        super().__init__(entity, keys.blood_tomb, 0, 0, (2, 3), description)


    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        
        self.entity.strength = max(0, min(20, self.entity.strength - max(1, self.effect_strength // 2)))
        self.entity.Update_Rune_Power(self.effect_strength) 

        if self.update_trigged:
            self.entity.game.inventory.rune_inventory.Set_Descriptions()


        return True
