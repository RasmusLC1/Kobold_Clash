from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Reduces damage that entity takes, cannot fully cancel damage though
class Resistance(Effect):
    def __init__(self, entity):
        description = 'General damage\nresistance'
        super().__init__(entity, keys.resistance, 0, 0, (3, 4), description)
        self.entity_health_holder = entity.health

    
    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        
        if self.entity.health < self.entity_health_holder:
            self.entity.health = min(self.entity.health + self.effect, self.entity_health_holder - 2)
        
        self.entity_health_holder = self.entity.health
        return True
    
    def Damage_Taken(self, damage):
        entity = self.entity
        # entity always take at least 2 damage
        new_health = min(entity.health + self.effect, self.entity_health_holder - 2)
        entity.Set_Health(new_health)
        self.entity_health_holder = entity.health
    
    