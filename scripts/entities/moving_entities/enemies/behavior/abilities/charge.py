from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys

COOLDOWN_TIME = 50
# Increases speed when enemy spots the player
class Charge(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.speed, self.entity.agility)
        return True
        
    # Returns true if entity is damaged 30% of health
    def Check_If_Trigger(self):
        return self.entity.player_spotted