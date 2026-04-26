
from scripts.entities.moving_entities.enemies.behavior.abilities.special_attack import Ability
from scripts.engine.keys.keys import keys

COOLDOWN_TIME = 10
class Run_Away(Ability):
    def __init__(self, game, entity):
        super().__init__(game, entity)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        if not super().Activate():
            return False
        
        self.entity.Set_Effect(keys.speed, 3)
        return True
    

    def _Check_If_Trigger(self):
        return self.entity.damaged