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


    def Set_Entity_Image(self):
        self.Set_Sprite()
        if not self.sprite:
            return
        self.entity_image = self.sprite[self.animation_value]

    # Set the idle state every 60 ticks to either up or down depending on last input
    def Set_Idle(self):
        if self.entity.direction_y_holder < 0:
            self.Set_Animation('idle_up')
        else:
            self.Set_Animation('idle_down')


    def Handle_Animation_Update(self, delta_time) -> None:
        if keys.attack in self.animation:
            self.Update_Attack_Animation(delta_time)
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