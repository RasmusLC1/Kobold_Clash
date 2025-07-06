from scripts.traps.trap import Trap

import random
from scripts.engine.keys.keys import keys


class Ice(Trap):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
        self.animation = random.randint(0, 1)

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

            if self.type == keys.shallow_ice_env:
                entity.On_Ice(20)
            elif self.type == keys.medium_ice_env:
                entity.On_Ice(20)
            elif self.type == keys.deep_ice_env:
                entity.On_Ice(20)


