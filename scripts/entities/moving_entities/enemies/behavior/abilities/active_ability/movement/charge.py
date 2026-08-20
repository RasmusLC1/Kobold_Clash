from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.active_ability import Active_Ability
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability


COOLDOWN_TIME = 50
# Increases speed when enemy spots the player
@register_ability(keys.charge) # add ability to registry
class Charge(Active_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, can_attack_while_triggered=True)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.speed, self.entity.agility)
        return True
        
    # Returns true if entity is damaged 30% of health
    def Check_If_Trigger(self):
        return self.entity.target_spotted