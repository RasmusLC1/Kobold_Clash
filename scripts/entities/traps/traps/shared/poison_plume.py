from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import random

class Poison_Plume(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.poison_plume)
        self.animation = 0

    def Update(self, delta_time, entity = None):

        if entity.category == keys.item:
            return

        if self.rect().colliderect(entity.rect()) and self.cooldown == 0 and self.animation > 3:
            if entity.Get_Effect_Strength(keys.invulnerable):
                return
            entity.Damage_Taken(2, (keys.poison, 0))
            # entity.Set_Effect('slow_down', 4)
            

    def Animation_Update(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time

        if self.animation_cooldown == 0:
            if self.animation >= 5:
                self.animation = 0
            else:
                self.animation += 1
            
            self.animation_cooldown = random.randint(0.3, 0.4)