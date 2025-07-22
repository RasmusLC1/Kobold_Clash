from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_explosion import Elemental_Explosion
from scripts.engine.keys.keys import keys

class Poison_Cloud(Elemental_Explosion):
    def __init__(self, game, pos, power, entity):
        super().__init__(game, keys.poison_cloud, keys.poison, pos, power, 4, 3, 0.4, entity)
        self.poison_cooldown = 0
        self.poison_cooldown_max = 10
        self.delete_countdown = self.max_animation * self.animation_cooldown_max * max(self.power // 2, 1)


    def Poison_Entities(self):
        if self.poison_cooldown < self.poison_cooldown_max:
            self.poison_cooldown += 1
            return
        self.poison_cooldown = 0
        for entity in self.nearby_entities:
            entity.effects.Set_Effect(self.effect, 1)



    def Update(self, update_pos = True):
        if update_pos:
            self.pos = list(self.entity.rect().center)
        self.Poison_Entities()
        return super().Update()
