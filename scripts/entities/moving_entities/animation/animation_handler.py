from scripts.engine.keys.keys import keys

class Animation_Handler():

    def __init__(self, entity):
        # Handle regular animation
        self.entity = entity
        self.sprite = None
        self.entity_image = None
        self.animation_value = 0
        self.flip = [False, False]
        self.action = ''
        self.animation_value = 0


        self.animation_lock = False
        self.Set_Animation('')


        self.animation_num = 0
        self.animation_num_max = 0
        self.animation_num_cooldown = 0
        self.animation_num_cooldown_max = 0.8

        # Handle attack animations
        self.attack_animation_num = 0
        self.attack_animation_num_max = 0
        self.attack_animation_num_cooldown = 0
        self.attack_animation_num_cooldown_max = 0.2


         # Jumping attack
        self.jumping_animation_num = 0
        self.jumping_animation_num_max = 0
        self.jumping_animation_num_cooldown = 0
        self.jumping_animation_num_cooldown_max = 0.8


    def Set_Sprite(self):
        self.sprite = self.entity.game.assets[self.animation]

    # Setting the item image and scaling it
    def Set_Entity_Image(self):
        try:
            self.entity_image = self.sprite[self.animation_value]
            # self.entity_image = pygame.transform.scale(entity_image, self.entity.size)
        except Exception as e:
            print(f'ANIMATION WENT WRONG {e}', self.sprite, self.animation_value, self.animation)
        

    # Set new action for animation
    def Set_Animation(self, action):
        if self.animation_lock:
            return
        
        if action != self.entity.action:
            self.entity.action = action
            self.animation = self.entity.type + '_' + self.entity.action
            self.animation_num = 0
            self.attack_animation_num = 0
            self.animation_value = 0
            self.jumping_animation_num = 0
            self.Set_Sprite()
            self.Set_Animation_Lock(True)

    # Set the idle state every 60 ticks to either up or down depending on last input
    def Set_Idle(self):
        return
    

    def Handle_Animation_Update(self, delta_time) -> None:
        if keys.attack in self.animation:
            self.Update_Attack_Animation(delta_time)
        elif 'jumping' in self.animation:
            self.Update_Jumping_Animation(delta_time)
        else:
            self.Update_Animation(delta_time)

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

    def Update_Attack_Animation(self, delta_time) -> None:
        if self.attack_animation_num_cooldown > 0:
            self.attack_animation_num_cooldown = max(0, self.attack_animation_num_cooldown - delta_time)
            return
        
        self.attack_animation_num_cooldown = self.attack_animation_num_cooldown_max
        self.attack_animation_num += 1


        if self.attack_animation_num == self.attack_frame:
            self.entity.Trigger_Attack()

        if self.attack_animation_num > self.attack_animation_num_max:
            self.attack_animation_num = 0
            self.Set_Animation_Lock(False)


        self.Set_Entity_Image()
        self.animation_value = self.attack_animation_num

    

    def Update_Jumping_Animation(self, delta_time) -> None:
        if self.jumping_animation_num_cooldown > 0:
            self.jumping_animation_num_cooldown = max(0, self.jumping_animation_num_cooldown - delta_time)
            return

        self.jumping_animation_num_cooldown = self.jumping_animation_num_cooldown_max
        self.jumping_animation_num += 1
        self.Set_Entity_Image()

        if self.jumping_animation_num > self.jumping_animation_num_max:
            self.jumping_animation_num = 0  # Reset animation
            self.Set_Animation_Lock(False)

        self.animation_value = self.jumping_animation_num


    def Set_Attack_Frame(self, attack_frame):
        self.attack_frame = attack_frame


    def Set_Animation_Num_Max(self, value):
        self.animation_num_max = value

    def Set_Attack_Animation_Num_Max(self, value):
        self.attack_animation_num_max = value
        self.Set_Attack_Frame(max(0, value - 1))
        self.Set_Attack_Animation_Num_Cooldown_Max(value)

    def Set_Junmp_Animation_Num_Max(self, value):
        self.jumping_animation_num_max = value

    def Set_Animation_Num_Cooldown_Max(self, value):
        self.animation_num_cooldown_max = value

    def Set_Attack_Animation_Num_Cooldown_Max(self, attack_animations):
        self.attack_animation_num_cooldown_max = self.entity.max_weapon_charge / attack_animations

    def Set_Junmp_Animation_Num_Cooldown_Max(self, value):
        self.jumping_animation_num_cooldown_max = value

    def Set_Animation_Lock(self, state):
        self.animation_lock = state