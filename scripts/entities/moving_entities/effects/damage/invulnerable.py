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
        
        if not super().Set_Effect(effect_time, permanent):
            return False
        
        # Treat invulnerable as an ability as it affects movement and damage
        self.entity.Set_Active_Ability(keys.invulnerable)
        self.entity_health_holder = self.entity.health

        return True
    
    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        
        self.entity.frame_movement = (0, 0)
        return True

    
    def Remove_Effect(self, reduce_permanent=0):
        disable_invulnerable = super().Remove_Effect(reduce_permanent)
        if disable_invulnerable:
            self.entity.Remove_Active_Ability()

        return disable_invulnerable


    
    def Damage_Taken(self, damage):
        self.entity.Set_Health(self.entity_health_holder)

    def Push(self, direction):
        self.entity.Set_Frame_movement((0, 0)) # Cancel frame movementaw