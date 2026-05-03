from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Immune to damage but cannot move
class Invulnerable(Effect):
    def __init__(self, entity):
        description = 'Prevents all damage\nbut snare'
        super().__init__(entity, keys.invulnerable, 0, 0, (0.5, 0.8), description)
        self.entity_health_holder = entity.health

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        # Treat invulnerable as an ability as it affects movement and damage
        if not self.entity.Set_Active_Ability(keys.invulnerable):
            return False
        
        if not super().Set_Effect(effect_time, permanent):
            return False
        
        self.entity_health_holder = self.entity.health
        self.entity.effects.Set_Effect(keys.snare, self.cooldown)

        return True
    
    def Update_Effect(self, delta_time):
        if not self.effect:
            return False
        
        self.Update_Cooldown(delta_time)

        return True
    
    def Remove_Effect(self, reduce_permanent=0):
        state = super().Remove_Effect(reduce_permanent)
        if state:
            self.entity.effects.Set_Effect(keys.snare, -10)
            self.entity.Remove_Active_Ability()

        return state
    
    def Damage_Taken(self, damage):
        self.entity.Set_Health(self.entity_health_holder)