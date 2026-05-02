from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys


COOLDOWN_TIME = 50
class Invincible(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.invulnerable, 5)
        return COOLDOWN_TIME
        
    # Returns true if entity is damaged 30% of health
    def Check_If_Trigger(self):
        index = self.entity.Get_Health_Index()
        return index > 1