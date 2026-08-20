from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.active_ability import Active_Ability
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys



COOLDOWN_TIME = 30

@register_ability(keys.rage) # add ability to registry
class Rage(Active_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, can_attack_while_triggered=True)
        self.rage_time = 0
        self.rage_strength_bonus = 3

    def Save_Data(self):
        super().Save_Data()
        self.entity.saved_data['rage_time'] = self.rage_time
        self.entity.saved_data['rage_strength_bonus'] = self.rage_strength_bonus

    def Load_Data(self, data):
        self.rage_time = data['rage_time']
        self.rage_strength_bonus = data['rage_strength_bonus']
        super().Load_Data(data)


    def Activate(self):
        self.entity.Set_Behavior_Pattern(keys.direct)
        self.entity.Trigger_Instant_Attack()
        self.entity.Set_Effect(keys.increase_strength, self.rage_strength_bonus)
        self.rage_time = 5 # 10 seconds of rage
        return True

    def Update(self, delta_time):
        if self.rage_time:
            self.Update_Rage_Timer(delta_time)

        return super().Update(delta_time)    
    
    def Update_Rage_Timer(self, delta_time):
        if self.rage_time <= 0:
            self._Reset_Attack()
            return False
        
        self.rage_time -= delta_time
        return True

    def _Reset_Attack(self):
        self.rage_time = 0
        self.entity.Reset_Attack_Speed()
        self.entity.Reset_Behavior()
        self._Set_Cooldown()
        
        # Returns true if entity is damaged
    def Check_If_Trigger(self):
        index = self.entity.Get_Health_Index()
        return index > 5
            