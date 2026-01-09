from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Powerful life steal but slowly drains you
class Blood_Ring(Effect):
    def __init__(self, entity):
        description = 'Powerful life steal\nbut slowly drains you'
        super().__init__(entity, keys.blood_ring, 0, 0, (5, 7), description)


    def Damage_Dealt(self, damage):
        modifier = 10 - self.effect
        damage_heal = max(1, damage // modifier) * 3 # 3 times as efficient 
        self.entity.Set_Effect(keys.healing, damage_heal)
    
    def Damage_Entity(self):
        self.entity.Damage_Taken(self.effect, (keys.vampiric, 1))

    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        
        if self.update_trigged:
            self.update_trigged = False
            self.Damage_Entity()
            
        return True