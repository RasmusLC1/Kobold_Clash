from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.dash_attacks.dash import Dash
from scripts.engine.keys.keys import keys

class Jump_Attack(Dash):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, min_distance=100, max_distance=200, speed_factor=13)
        self.wait_before_jump_cooldown = 0
        self.jump_trigged = False

    def Save_Data(self):
        super().Save_Data()
        self.entity.saved_data['wait_before_jump_cooldown'] = self.wait_before_jump_cooldown
        self.entity.saved_data['jump_trigged'] = self.jump_trigged

    def Load_Data(self, data):
        self.wait_before_jump_cooldown = data['wait_before_jump_cooldown']
        self.jump_trigged = data['jump_trigged']
        super().Load_Data(data)


    def Update(self, delta_time):
        if self.Update_Wait_Before_Jumping(delta_time):
            return
        
        return super().Update(delta_time)
    

    def Update_Wait_Before_Jumping(self, delta_time):
        if self.jump_trigged:
            return False
        
        if self.wait_before_jump_cooldown <= 0:
            self.wait_before_jump_cooldown = 0
            self.jump_trigged = True
            self.Calculate_Direction() # calculate the location again
            return False
        
        self.wait_before_jump_cooldown -= delta_time
        self.entity.Reduce_Movement(10000) # Prevents the enemy from moving while jump charges
        return True

    def Calculate_Direction(self):
        if self.wait_before_jump_cooldown > 0:
            return
        return super().Calculate_Direction()

    def Activate(self):
        self.wait_before_jump_cooldown = (10 - self.entity.agility) / 5  # wait time before jumping
        self.entity.Set_Touching_Ground(False)
        return super().Activate()
    
    def _Reset_Attack(self):
        self.entity.Set_Touching_Ground(True)
        self.jump_trigged = False
        return super()._Reset_Attack()