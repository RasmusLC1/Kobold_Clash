from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.engine.keys.keys import keys

class Player_Animation_Handler(Animation_Handler):
    def __init__(self, entity):
        super().__init__(entity)
                 # Jumping attack
        self.rolling_animation_num = 0
        self.rolling_animation_num_max = 4
        self.rolling_animation_num_cooldown = 0
        self.rolling_animation_num_cooldown_max = 0.2
        self.Set_Idle_Num_Max(3)
        self.Set_Idle_Animation_Num_Cooldown_Max(0.2)
        self.Set_Animation_Num_Cooldown_Max(0.1)
        self.Set_Animation_Num_Max(5)



        

    # Set the idle state every 60 ticks to either up or down depending on last input
    def Set_Idle(self):
        if self.entity.direction_y_holder < 0:
            self.Set_Animation('idle_up')
        else:
            self.Set_Animation('idle_down')


    def Set_Action(self):
        keyboard = self.game.keyboard_handler
        if not keyboard.Check_If_Movement_Enabled():
            if self.direction_y_holder < 0:
                self.animation_handler.Set_Animation('standing_still_up')
            else:
                self.animation_handler.Set_Animation('standing_still_down')
            return

        self.idle_count = 0

        if keyboard.w_pressed:
            self.animation_handler.Set_Animation('running_up')
        else:
            self.animation_handler.Set_Animation('running_down')

    def Handle_Animation_Update(self, delta_time) -> None:
        if keys.attack in self.animation:
            self.Update_Attack_Animation(delta_time)
        elif 'standing_still' in self.animation:
            self.Update_Idle_Animation(delta_time)
        elif 'roll' in self.animation:
            self.Update_Roll_Animation(delta_time)
        else:
            self.Update_Animation(delta_time)

    def Update_Attack_Animation(self, delta_time) -> None:
        if self.attack_animation_num_cooldown > 0:
            self.attack_animation_num_cooldown = max(0, self.attack_animation_num_cooldown - delta_time)
            return
        
        self.attack_animation_num_cooldown = self.attack_animation_num_cooldown_max
        self.attack_animation_num += 1

        if self.attack_animation_num > self.attack_animation_num_max:
            self.attack_animation_num = 0
            self.Set_Animation_Lock(False)


        self.Set_Entity_Image()
        self.animation_value = self.attack_animation_num

    def Update_Roll_Animation(self, delta_time):
        if self.rolling_animation_num_cooldown > 0:
            self.rolling_animation_num_cooldown = max(0, self.rolling_animation_num_cooldown - delta_time)
            return
        
        self.rolling_animation_num_cooldown = self.rolling_animation_num_cooldown_max
        self.rolling_animation_num += 1

        if self.rolling_animation_num > self.rolling_animation_num_max:
            self.rolling_animation_num = 0
            self.Set_Animation_Lock(False)


        self.Set_Entity_Image()
        self.animation_value = self.rolling_animation_num


    def Update_Animation(self, delta_time) -> None:
        if self.animation_num_cooldown > 0:
            self.animation_num_cooldown = max(0, self.animation_num_cooldown - delta_time)
            return
        self.animation_num_cooldown = self.animation_num_cooldown_max
        self.animation_num += 1
        if self.animation_num > self.animation_num_max:
            self.animation_num = 0
            self.Set_Animation_Lock(False)

        self.Set_Entity_Image()
        self.animation_value = self.animation_num


    
    def Update_Idle_Animation(self, delta_time) -> None:
        if self.idle_animation_num_cooldown > 0:
            self.idle_animation_num_cooldown = max(0, self.idle_animation_num_cooldown - delta_time)
            return

        self.idle_animation_num_cooldown = self.idle_animation_num_cooldown_max
        self.idle_animation_num += 1

        if self.idle_animation_num > self.idle_animation_num_max:
            self.idle_animation_num = 0  # Reset animation
            self.Set_Animation_Lock(False)

        self.Set_Entity_Image()
        self.animation_value = self.idle_animation_num
