
from scripts.entities.moving_entities.enemies.behavior.special_attacks.special_attack import Special_Attack
from scripts.engine.keys.keys import keys

COOLDOWN_TIME = 10
class Run_Away(Special_Attack):
    def __init__(self, game, entity):
        super().__init__(game, entity)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        if not super().Activate():
            return False
        
        self.entity.Set_Effect(keys.speed, 3)
        return True