from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Long lasting damage and weakens the entity
class Poison(Effect):
    def __init__(self, entity):
        description = 'poison Damage over time,\nreduces increase_strength'
        super().__init__(entity, keys.poison, 2, 0.4, (1, 1.2), description)
        self.strength_holder = self.entity.strength

    
    #set Fire effect
    def Set_Effect(self, effect_time, permanent = False):
        if self.Get_Entity_Effect_Strength(keys.poison_resistance):
            return False
        
        if not super().Set_Effect(effect_time, permanent):
            return False
        
        self.entity.Set_Healing_Enabled(False)
        return True

    
    def Remove_Effect(self, reduce_permanent=0):
        if not super().Remove_Effect(reduce_permanent):
            return False
        self.entity.Set_Healing_Enabled(True)
        return True
        

    def Update_Effect(self, delta_time):
        # Enable healing when poison expires
        if not self.effect_strength:
            self.entity.Set_Healing_Enabled(True)
            return False
        self.entity.Set_Strength(self.strength_holder // 2)

        if self.Get_Entity_Effect_Strength(keys.poison_resistance):
            self.effect_strength = 0
            self.cooldown = 0
            self.entity.Set_Healing_Enabled(True)
            return False
        

        if self.Update_Cooldown(delta_time):
            self.entity.Damage_Taken(self.effect_strength, (self.effect_type, 0))

        self.Effect_Animation_Cooldown(delta_time)
        return True
    
    