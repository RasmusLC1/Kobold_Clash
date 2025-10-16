from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.engine.keys.keys import keys

class Player_Animation_Handler(Animation_Handler):
    def __init__(self, entity):
        super().__init__(entity)


        self.keyboard = self.entity.game.keyboard_handler

        # Add player-specific animations to unified handler
        self.animations.update({
            keys.roll: {keys.num: 0, keys.num_max: 4, keys.cooldown: 0, keys.cooldown_max: 0.2},
            keys.backstep: {keys.num: 0, keys.num_max: 4, keys.cooldown: 0, keys.cooldown_max: 0.2},
        })

        # Player animation timings
        self.Set_Animation_Num_Max(keys.idle, 3)
        self.Set_Animation_Cooldown_Max(keys.idle, 0.2)
        self.Set_Animation_Num_Max(keys.run, 5)
        self.Set_Animation_Cooldown_Max(keys.run, 0.1)

        self.Set_Animation_Num_Max(keys.attack, 4)
        self.Set_Animation_Cooldown_Max(keys.attack, 0.1)

    # State Handling 
    def Set_Action(self):
        if self.animation_lock:
            return
        if self.Check_Special_Animations(): # Check special first as this is priority
            return

        if self.Check_Movement():
            return


    # Check general movement and idling
    def Check_Movement(self):
        keyboard = self.keyboard
        if not keyboard.Check_If_Movement_Enabled():
            self.Set_Animation('idle_down')
            return False

        if keyboard.w_pressed:
            if keyboard.d_pressed:
                self.flip[0] = False
            else:
                self.flip[0] = True
            self.Set_Animation('running_up')
        else:
            self.Set_Animation('running_down')

        return True
    


    # Check for special animations, such as attacks and special movements
    def Check_Special_Animations(self):
        keyboard = self.keyboard
        if keyboard.space_pressed:
            self.Set_Animation("rolling")
            self.Set_Animation_Lock(True)
            return True

        if keyboard.alt_pressed:
            self.Set_Animation(keys.backstep)
            self.Set_Animation_Lock(True)
            return True

        return False


    def Trigger_Attack_Animation(self):
        self.Attack_Direction_Handler()
        self.Set_Animation("attack")
        self.Set_Animation_Lock(True)
        return True
        

    def Set_Animation(self, action):
        if self.animation_lock:
            return

        if action != self.entity.action:
            self.entity.action = action
            self.animation = self.entity.type + '_' + self.entity.action
            for anim in self.animations.values():
                anim[keys.num] = 0
            self.animation_value = 0
            self.Set_Sprite()

    # Animation Updates
    def Handle_Animation_Update(self, delta_time):
        for anim_type in self.animations.keys():
            if anim_type in self.animation:
                self.Update_Generic_Animation(anim_type, delta_time)
                return
        # fallback if no match
        self.Update_Generic_Animation(keys.idle, delta_time)

