from scripts.engine.keys.keys import keys

class Animation_Handler:
    def __init__(self, entity):
        self.entity = entity
        self.sprite = None
        self.entity_image = None
        self.animation_value = 0
        self.flip = [False, False]
        self.action = ''
        self.animation_lock = False
        self.Set_Animation('')

        # Unified animation data
        self.animations = {
            keys.run: {keys.num: 0, keys.num_max: 0, keys.cooldown: 0, keys.cooldown_max: 0.1},
            keys.attack: {keys.num: 0, keys.num_max: 0, keys.cooldown: 0, keys.cooldown_max: 0.2},
            keys.jump: {keys.num: 0, keys.num_max: 0, keys.cooldown: 0, keys.cooldown_max: 0.2},
            keys.idle: {keys.num: 0, keys.num_max: 0, keys.cooldown: 0, keys.cooldown_max: 0.2}
        }

        self.attack_frame = 0

    def Set_Sprite(self):
        self.sprite = self.entity.game.assets[self.animation]

    def Set_Entity_Image(self):
        try:
            self.entity_image = self.sprite[self.animation_value]
        except Exception as e:
            print(f'ANIMATION WENT WRONG {e}', self.sprite, self.animation_value, self.animation)

    def Update_Animation(self, delta_time):
        self.Set_Action()
        self.Handle_Animation_Update(delta_time)

    def Set_Action(self):
        entity = self.entity
        if entity.distance_to_player > 300:
            return

        if entity.charge > 0:
            self.Set_Animation(keys.attack)
        elif entity.frame_movement:
            self.Set_Animation('running')
        else:
            self.Set_Animation('idle')

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
            self.Set_Animation_Lock(True)

    def Handle_Animation_Update(self, delta_time):
        for anim_type in self.animations.keys():
            if anim_type in self.animation:
                self.Update_Generic_Animation(anim_type, delta_time)
                break

    def Update_Generic_Animation(self, anim_type, delta_time):
        anim = self.animations[anim_type]
        if anim[keys.cooldown] > 0:
            anim[keys.cooldown] = max(0, anim[keys.cooldown] - delta_time)
            return

        anim[keys.cooldown] = anim[keys.cooldown_max]
        anim[keys.num] += 1

        if anim[keys.num] > anim[keys.num_max]:
            anim[keys.num] = 0
            self.Set_Animation_Lock(False)

        if anim_type == keys.attack and anim[keys.num] == self.attack_frame:
            self.entity.Trigger_Attack()

        self.animation_value = anim[keys.num]
        self.Set_Entity_Image()

    # --- Generalized setter functions ---
    def Set_Animation_Num_Max(self, anim_type, value):
        if anim_type in self.animations:
            self.animations[anim_type][keys.num_max] = value

    def Set_Animation_Cooldown_Max(self, anim_type, value):
        if anim_type in self.animations:
            self.animations[anim_type][keys.cooldown_max] = value

    # Attack-specific because it depends on entity stats
    def Set_Attack_Animation_Num_Max(self, value):
        self.Set_Animation_Num_Max(keys.attack, value)
        self.attack_frame = max(0, value - 1)
        self.Set_Animation_Cooldown_Max(keys.attack, self.entity.max_weapon_charge / value)

    def Set_Attack_Frame(self, attack_frame):
        self.attack_frame = attack_frame

    def Set_Animation_Lock(self, state):
        self.animation_lock = state
