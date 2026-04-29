from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys


COOLDOWN_TIME = 10
class Invincible(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.speed, 3)
        return COOLDOWN_TIME
        