
from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys

COOLDOWN_TIME = 10
class Run_Away(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        if not super().Activate():
            return False
        
        self.entity.Set_Effect(keys.speed, 3)
        self.entity.Set_Retreat()
        self._Set_Cooldown()
        return True
    
    # Returns true if entity is damaged
    def Check_If_Trigger(self):
        return self.entity.damaged