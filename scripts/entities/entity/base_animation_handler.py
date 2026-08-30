import random

class Base_Animation_Handler:
    def __init__(self, entity, animation_max, animation_cooldown_max):
        self.entity = entity
        self.sprite = None
        self.animation = 0
        self.min_animation = 0
        self.animation_max = int(animation_max)
        self.animation_cooldown = 0.0
        self.animation_cooldown_max = float(animation_cooldown_max)
        self.Set_Random_Animation()

    def Save_Data(self):
        return {
            'animation': self.animation,
            'animation_cooldown': self.animation_cooldown
        }

    def Load_Data(self, data):
        self.animation = data['animation']
        self.animation_cooldown = data['animation_cooldown']

    def Set_Sprite(self, key):
        try:
            self.sprite = self.entity.game.assets[key]
        except Exception as e:
            print(f'Setting sprite failed: {e}', getattr(self.entity, 'type', None), key)
            return False
        self.Set_Entity_Image()
        return True

    def Set_Entity_Image(self):
        if not self.sprite:
            return
        try:
            self.entity.entity_image = self.sprite[self.animation].convert_alpha()
            self.entity.render_needs_update = True
        except Exception as e:
            print(f'Set entity image failed: {e}', getattr(self.entity, 'type', None), self.animation, self.sprite)

    def Set_Frame(self, value):
        value = max(0, min(int(value), self.animation_max))
        self.animation = value
        self.Set_Entity_Image()

    def Increase_Frame(self):
        next_value = self.animation + 1
        if next_value > self.animation_max:
            next_value = self.min_animation
        self.Set_Frame(next_value)

    def Update_Animation(self, movement, delta_time):
        if not self.entity.render:
            return False
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
            return False
        
        self.Increase_Frame()
        self.animation_cooldown = self.animation_cooldown_max
        return True

    def Set_Random_Animation(self):
        if self.animation_max > 0:
            self.animation = random.randint(self.min_animation, self.animation_max)
        else:
            self.animation = 0

    