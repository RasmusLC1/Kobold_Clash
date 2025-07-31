from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import pygame

class Spike_Pit(Trap):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
        self.slow_amount = 4


    def Update(self, delta_time):
        if not super().Update(delta_time):
            return False
        
        if not self.Update_Cooldown(delta_time):
            return
        self.Update_Trapped_Entities()
        return True
        
        
    def Update_Trapped_Entities(self):
        for entity in self.entities:
            if not self.rect().colliderect(entity.rect()):
                self.entities.remove(entity)
                entity.Remove_Effect(keys.slow, self.slow_amount)
                continue

            if entity.effects.invulnerable.effect:
                return
            entity.Damage_Taken(5)

    def Add_Entity_To_Trap(self, entity):
        if not super().Add_Entity_To_Trap(entity):
            return False
        # Trigger trap animation and snare
        if not self.animation:
            self.animation = 1
            entity.Set_Effect(keys.snare, 2)
        else:
            entity.Set_Effect(keys.slow, self.slow_amount)
        return True

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0]-5, self.size[1]-5)
                    
