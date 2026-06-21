from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys

class Healing_From_Damage_Type(Passive_Ability):
    def __init__(self, game, entity, name, effect_name):
        super().__init__(game, entity, name)
        self.effect_name = effect_name

    def Update(self, delta_time):
        self.Check_If_On_Fire()
        return super().Update(delta_time)
    

    def Check_If_On_Fire(self):
        entity = self.entity
        effect = entity.Get_Effect(self.effect_name)
        if not effect:
            return False
        
        entity.Set_Effect(keys.healing, effect.effect_strength)
        entity.Set_Effect(self.effect_name + '_resistance', 2)
        return True
    