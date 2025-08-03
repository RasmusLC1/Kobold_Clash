from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import random

CLATTER_RANGE = 500

class Rubble(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.rubble)
        self.animation = random.randint(0, 3)


    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return
        
        self.game.sound_handler.Play_Sound(keys.rubble, 0.4)
        self.game.clatter.Generate_Clatter(self.pos, CLATTER_RANGE) # Generate clatter to alert nearby enemies

            
