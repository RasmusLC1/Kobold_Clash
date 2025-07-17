from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_explosion import Elemental_Explosion
from scripts.engine.keys.keys import keys


class Ice_Explosion(Elemental_Explosion):
    def __init__(self, game, pos, power, entity = None):
        super().__init__(game, keys.ice_explosion, keys.frozen, pos, power, 5, 5, 5, entity)

    def Slow_Entities(self):
        for entity in self.nearby_entities:
            entity.effects.Set_Effect(keys.frozen, self.power)

    def Update_Animation(self, delta_time):
        self.Slow_Entities()

        return super().Update_Animation(delta_time)