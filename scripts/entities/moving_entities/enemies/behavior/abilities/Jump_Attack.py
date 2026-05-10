from scripts.entities.moving_entities.enemies.behavior.abilities.dash import Dash
from scripts.engine.keys.keys import keys

class Jump_Attack(Dash):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, min_distance=100, max_distance=200, speed_factor=13)
        self.wait_before_jump_cooldown = 0


    def Update(self, delta_time):
        if self.Update_Wait_Before_Jumping(delta_time):
            return
        
        return super().Update(delta_time)
    

    def Update_Wait_Before_Jumping(self, delta_time):
        if self.wait_before_jump_cooldown <= 0:
            self.wait_before_jump_cooldown = 0
            return False
        
        self.wait_before_jump_cooldown -= delta_time
        self.entity.Reduce_Movement(10000) # Prevents the enemy from moving while jump charges
        return True



    def Activate(self):
        self.wait_before_jump_cooldown = (10 - self.entity.agility) / 5  # wait time before jumping
        self.entity.Set_Touching_Ground(False)
        return super().Activate()
    
    def _Reset_Attack(self):
        self.entity.Set_Touching_Ground(True)
        return super()._Reset_Attack()