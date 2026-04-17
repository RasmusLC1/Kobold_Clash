
from scripts.engine.keys.keys import keys


COOLDOWN_TIME = 10
class Run_Away():

    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.speed, 3)
        return COOLDOWN_TIME