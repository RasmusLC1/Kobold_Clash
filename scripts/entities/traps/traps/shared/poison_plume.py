from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import random

class Poison_Plume(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.poison_plume, max_animation=5, animation_cooldown_max=0.4)

    def Update(self, delta_time, entity = None):

        if entity.category == keys.item:
            return

        if self.rect().colliderect(entity.rect()) and self.cooldown == 0 and self.animation > 3:
            if entity.Get_Effect_Strength(keys.invulnerable):
                return
            entity.Damage_Taken(2, (keys.poison, 0))
            # entity.Set_Effect('slow_down', 4)
            
