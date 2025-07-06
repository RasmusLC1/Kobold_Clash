from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Immune to damage but cannot move
class Player_Movement_Invunerable(Effect):
    def __init__(self, entity):
        super().__init__(entity, keys.invulnerable, 0, 0, (30, 50), '')
        self.entity_health_holder = entity.health

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.effect:
            return
        self.entity_health_holder = self.entity.health
        self.effect = effect_time
    
    def Update_Effect(self):
        if not super().Update_Effect():
            return False

        
        if self.entity.health < self.entity_health_holder:
            self.entity.health = self.entity_health_holder
    
        self.entity_health_holder = self.entity.health
        return False