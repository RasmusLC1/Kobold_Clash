from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import pygame

class Spike_Pit(Trap):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
        self.slow_amount = 1
        

    def Apply_Entity_Effect(self, entity):
        if not self.animation:
            self.animation = 1
            entity.Damage_Taken(10, (keys.snare, 2))
        else:
            entity.Damage_Taken(5, (keys.slow, self.slow_amount))



    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0]-5, self.size[1]-5)
                    
