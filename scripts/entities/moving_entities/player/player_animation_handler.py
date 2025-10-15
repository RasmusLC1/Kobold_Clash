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
        self.keyboard = self.entity.game.keyboard_handler



    # Set the idle state every 60 ticks to either up or down depending on last input
    def Set_Idle(self):
        if self.entity.direction_y_holder < 0:
            self.Set_Animation('idle_up')
        else:
            self.Set_Animation('idle_down')


    def Set_Action(self):
        if self.Check_Movement(self.keyboard):
            return
        
        if self.Check_Special_Animations(self.keyboard):
            return



    def Check_Movement(self, keyboard):
        if not keyboard.Check_If_Movement_Enabled():
            self.Set_Animation('standing_still_down')
            return False

        if keyboard.w_pressed:
            self.Set_Animation('running_up')
        else:
            self.Set_Animation('running_down')
        return True
    
    def Check_Special_Animations(self, keyboard):
                # TODO: Needs animation
        if keyboard.alt_pressed:
            self.Set_Animation('backstep')
            self.Set_Animation_Lock(True)
            return True

        if keyboard.space_pressed:
            self.Set_Animation('rolling')
            self.Set_Animation_Lock(True)
            return True

        # TODO: Needs animation
        if keyboard.alt_pressed:
            self.Set_Animation('backstep')
            self.Set_Animation_Lock(True)
            return True
        
        return False

    def Handle_Animation_Update(self, delta_time) -> None:
        if keys.attack in self.animation:
            self.Update_Attack_Animation(delta_time)
        elif 'standing_still' in self.animation:
            self.Update_Idle_Animation(delta_time)
        elif 'roll' in self.animation:
            self.Update_Roll_Animation(delta_time)
        else:
            self.Update_Running_Animation(delta_time)

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



