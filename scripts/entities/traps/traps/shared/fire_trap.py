from scripts.entities.traps.trap import Trap

import random
from scripts.engine.keys.keys import keys


class Fire_Trap(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.fire_trap)
        self.animation = random.randint(0, 13)

    def Update(self, entity):
        if self.Cooldown > 0:
            self.Cooldown -= 1
        
        if entity.category == keys.item:
            return

        if self.rect().colliderect(entity.rect()) and self.Cooldown == 0 and self.animation > 7 and self.animation < 11:
            if entity.Get_Effect_Strength(keys.invulnerable):
                return
                
            entity.Set_Effect(keys.fire, 3)
            self.Cooldown = 100
                
    def Animation_Update(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
            return

        if self.animation >= 13:
            self.animation = 0
        else:
            self.animation += 1
        
        self.animation_cooldown = random.randint(0.1, 0.2)