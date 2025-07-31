from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import random

class Spike(Trap):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
        self.animation = random.randint(0, 5)
        self.slow_amount = 2


    def Update(self, delta_time):
        if not super().Update(delta_time):
            return False
        
        if not self.Update_Cooldown(delta_time):
            return
        self.Update_Trapped_Entities()
        return True
    
    def Add_Entity_To_Trap(self, entity):
        if not super().Add_Entity_To_Trap(entity):
            return False
        entity.Set_Effect(keys.slow, self.slow_amount)
        return True

        
    def Update_Trapped_Entities(self):
        for entity in self.entities:
            if not self.rect().colliderect(entity.rect()):
                self.entities.remove(entity)
                entity.Remove_Effect(keys.slow, self.slow_amount)

                continue

            if entity.effects.invulnerable.effect:
                return
            entity.Damage_Taken(2)            
            

    def Animation_Update(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
            return
        
        if self.animation >= 5:
            self.animation = 0
        else:
            self.animation += 1
        
        self.animation_cooldown = random.uniform(0.3, 0.4)