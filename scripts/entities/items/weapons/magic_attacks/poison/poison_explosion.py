from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_explosion import Elemental_Explosion
from scripts.engine.keys.keys import keys

class Poison_Explosion(Elemental_Explosion):
    def __init__(self, game, pos, power, entity = None):
        super().__init__(game, keys.poison_explosion, keys.poison, pos, power, 6, 5, 5, entity)
        self.poison_cooldown = 0
        self.poison_cooldown_max = 10

    def Poison_Entities(self):
        if self.poison_cooldown < self.poison_cooldown_max:
            self.poison_cooldown += 1
            return
        
        self.poison_cooldown = 0
        for entity in self.nearby_entities:
            entity.effects.Set_Effect(self.effect, 1)

    def Update_Animation(self):
        self.Poison_Entities()

        return super().Update_Animation()