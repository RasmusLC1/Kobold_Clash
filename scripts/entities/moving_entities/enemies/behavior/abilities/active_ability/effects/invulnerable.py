from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.active_ability import Active_Ability
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys




COOLDOWN_TIME = 50
@register_ability(keys.invulnerable) # add ability to registry
class Invulnerable(Active_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.invulnerable, 5)
        return True
    
    def Update(self, delta_time):
        if self.entity.active_ability != keys.invulnerable:
            self._Reset_Attack()
        return super().Update(delta_time)
        
    # Returns true if entity is damaged 30% of health
    def Check_If_Trigger(self):
        index = self.entity.Get_Health_Index()
        return index > 1