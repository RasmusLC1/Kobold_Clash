from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Don't generate sound and clatter
class Forsaken_Grimoire(Effect):
    def __init__(self, entity):
        description = 'Improves runes\nbut drains strength'
        super().__init__(entity, keys.blood_tomb, 0, 0, (2, 3), description)


    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        
        self.entity.strength = max(0, min(20, self.entity.strength - max(1, self.effect // 2)))
        self.entity.Update_Rune_Power(self.effect) 

        if self.update_trigged:
            self.entity.game.inventory.rune_inventory.Set_Descriptions()


        return True
