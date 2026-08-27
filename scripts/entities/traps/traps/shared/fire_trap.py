from scripts.entities.traps.trap import Trap

import random
from scripts.engine.keys.keys import keys


class Fire_Trap(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.fire_trap, max_animation=13, animation_cooldown_max=0.2)

    def Update(self, entity):
        if self.Cooldown > 0:
            self.Cooldown -= 1
        
        if entity.category == keys.item:
            return

        if self.rect().colliderect(entity.rect()) and self.Cooldown == 0 and self.animation > 7 and self.animation < 11:
            self.Entity_Hit(entity)
    
    def Entity_Hit(self, entity):
        if entity.Get_Effect_Strength(keys.invulnerable):
            return
            
        entity.Set_Effect(keys.fire, 3)
        self.Cooldown = 100
                
