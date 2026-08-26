from scripts.engine.keys.keys import keys
from scripts.entities.entity.animation_handler import Base_Animation_Handler

class Animation_Handler(Base_Animation_Handler):
    def __init__(self, entity, animation_max=0, animation_cooldown_max=0):
        super().__init__(entity, animation_max=animation_max,
                         animation_cooldown_max=animation_cooldown_max)
        self.animation_key = ''
        self.action = ''
        self.flip = [False, False]
        self.animation_lock = False

        self.animations = {
            keys.run: {keys.num: 0, keys.num_max: 0, keys.cooldown: 0, keys.cooldown_max: 0.1},
            keys.attack: {keys.num: 0, keys.num_max: 0, keys.cooldown: 0, keys.cooldown_max: 0.2},
            keys.jump: {keys.num: 0, keys.num_max: 0, keys.cooldown: 0, keys.cooldown_max: 0.2},
            keys.idle: {keys.num: 0, keys.num_max: 0, keys.cooldown: 0, keys.cooldown_max: 0.2}
        }
        self.attack_frame = 0
        self.Set_Animation('')

    def Update_Animation(self, movement, delta_time):
        self.Flip_Entity_In_Move_Direction(movement)
        self.Set_Action()
        self.Handle_Animation_Update(delta_time)

    def Set_Action(self):
        entity = self.entity
        if entity.distance_to_target > 300:
            return
        if entity.charge > 0:
            self.Set_Animation(keys.attack)
        elif entity.frame_movement:
            self.Set_Animation("running")
        else:
            self.Set_Animation(keys.idle)

    def Set_Animation(self, action):
        if self.animation_lock:
            return False
        if action != self.action:
            self.action = action
            self.animation_key = self.entity.type + '_' + self.action
            self.Reset_Animation_Values()
            self.animation = 0
            self.Set_Sprite(self.animation_key)
            self.Set_Animation_Lock(True)
            return True
        return False

    def Reset_Animation_Values(self):
        for anim in self.animations.values():
            anim[keys.num] = 0

    def Handle_Animation_Update(self, delta_time):
        for anim_type in self.animations.keys():
            if anim_type in self.animation_key:
                self.Update_Generic_Animation(anim_type, delta_time)
                break

    def Update_Generic_Animation(self, anim_type, delta_time):
        animation = self.animations[anim_type]
        if animation[keys.cooldown] > 0:
            animation[keys.cooldown] = max(0, animation[keys.cooldown] - delta_time)
            return False

        animation[keys.cooldown] = animation[keys.cooldown_max]
        animation[keys.num] += 1
        if animation[keys.num] > animation[keys.num_max]:
            animation[keys.num] = 0
            self.Set_Animation_Lock(False)

        if anim_type == keys.attack and animation[keys.num] == self.attack_frame:
            self.entity.Trigger_Attack()

        self.Set_Frame(animation[keys.num])
        return True

    # --- Generalized setter functions ---
    def Set_Animation_Num_Max(self, anim_type, value):
        if anim_type in self.animations:
            self.animations[anim_type][keys.num_max] = value

    def Set_Animation_Cooldown_Max(self, anim_type, value):
        if anim_type in self.animations:
            self.animations[anim_type][keys.cooldown_max] = value

            # Determine animation and flip based on movement
    def Flip_Entity_In_Move_Direction(self, movement):
        if movement[0] > 0:
            self.flip[0] = True
        elif movement[0] < 0:
            self.flip[0] = False

    def Attack_Direction_Handler(self):
        if self.entity.attack_direction[0] < 0:
            self.flip[0] = False
        else:
            self.flip[0] = True

    # Attack-specific because it depends on entity stats
    def Set_Attack_Animation_Num_Max(self, value):
        self.Set_Animation_Num_Max(keys.attack, value)
        self.attack_frame = max(0, value - 1)
        self.Set_Animation_Cooldown_Max(keys.attack, self.entity.max_weapon_charge / value)

    def Set_Attack_Frame(self, attack_frame):
        self.attack_frame = attack_frame

    def Set_Animation_Lock(self, state):
        self.animation_lock = state

    def Get_Action(self):
        return self.action