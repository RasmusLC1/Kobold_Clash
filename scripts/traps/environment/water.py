from scripts.traps.trap import Trap
from scripts.engine.keys.keys import keys
import random

class Water(Trap):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
        self.animation = random.randint(0, 2)

        self.Set_Slowdown_Amount()


    def Update(self):
        if not super().Update():
            return False
        
        if not self.Update_Cooldown():
            return
        self.Update_Trapped_Entities()
        return True
        
        
    def Update_Trapped_Entities(self):
        for entity in self.entities:
            if not self.rect().colliderect(entity.rect()):
                self.entities.remove(entity)
                continue

            entity.Set_Effect(keys.slow, self.slow_amount)
            entity.Set_Effect(keys.wet, 2)

    
    def Set_Slowdown_Amount(self):
        if self.type == keys.shallow_water_env:
            self.slow_amount = 2
        elif self.type == keys.medium_water_env:
            self.slow_amount = 4
        elif self.type == keys.deep_water_env:
            self.slow_amount = 8


    def Animation_Update(self):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= 1

        if self.animation_cooldown == 0:
            if self.animation >= 2:
                self.animation = 0
            else:
                self.animation += 1
            
            self.animation_cooldown = random.randint(20, 30)

    def Render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets[self.type][self.animation], (self.pos[0] - offset[0], self.pos[1] - offset[1]))