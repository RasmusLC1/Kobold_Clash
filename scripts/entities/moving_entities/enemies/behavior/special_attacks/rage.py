from scripts.entities.moving_entities.enemies.behavior.special_attacks.special_attack import Special_Attack
from scripts.engine.keys.keys import keys

COOLDOWN_TIME = 10
class Rage():

    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.speed, 3)
        return COOLDOWN_TIME