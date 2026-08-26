from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from ..traps.shared.shared_registry import register_trap
import random

@register_trap(keys.water_env) # no probablity as this needs to be spawned as lakes
class Water(Trap):
    def __init__(self, game, pos, type):
        super().__init__(game, pos, type)
        self.animation = random.randint(0, 2)

        self.Set_Slowdown_Amount()

        

    def Apply_Entity_Effect(self, entity):
        entity.Set_Effect(keys.slow, self.slow_amount)
        entity.Set_Effect(keys.wet, 2)

    
    def Set_Slowdown_Amount(self):
        if self.type == keys.shallow_water_env:
            self.slow_amount = 2
        elif self.type == keys.medium_water_env:
            self.slow_amount = 4
        elif self.type == keys.deep_water_env:
            self.slow_amount = 8


    def Animation_Update(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
            return

        if self.animation >= 2:
            self.animation = 0
        else:
            self.animation += 1
        
        self.animation_cooldown = random.uniform(0.4, 0.5)

    def Render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets[self.type][self.animation], (self.pos[0] - offset[0], self.pos[1] - offset[1]))