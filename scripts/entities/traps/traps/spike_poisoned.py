from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import random


class Spike_Poisoned(Trap):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
        self.animation = random.randint(0, 13)

        
    def Apply_Entity_Effect(self, entity):
        entity.Damage_Taken(2, (keys.poison, random.randint(3,5)))


    def Animation_Update(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
            return
        
        if self.animation >= 13:
            self.animation = 0
        else:
            self.animation += 1
        
        self.animation_cooldown = random.uniform(0.13, 0.15)
