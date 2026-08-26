class Base_Animation_Handler:
    def __init__(self, entity, animation_max, animation_cooldown_max):
        self.entity = entity
        self.sprite = None
        self.animation = 0
        self.animation_max = animation_max
        self.animation_cooldown = 0
        self.animation_cooldown_max = animation_cooldown_max

    def Save_Data(self):
        saved_data = {
            'animation': self.animation,
            'animation_cooldown': self.animation_cooldown
        }
        return saved_data

    def Load_Data(self, data):
        self.animation = data['animation']
        self.animation_cooldown = data['animation_cooldown']

    def Set_Sprite(self, key):
        try:
            self.sprite = self.entity.game.assets[key]
        except Exception as e:
            print(f'Setting sprite failed: {e}', self.entity.type, key)
            return False
        self.Set_Entity_Image()
        return True

    def Set_Entity_Image(self):
        try:
            self.entity.entity_image = self.sprite[self.animation].convert_alpha()
            self.entity.render_needs_update = True
        except Exception as e:
            print(f'Set entity image failed: {e}', self.entity.type, self.animation, self.sprite)

    def Set_Frame(self, value):
        value = min(value, self.animation_max)
        self.animation = value
        self.Set_Entity_Image()

    def Increase_Frame(self):
        next_value = self.animation + 1
        if next_value > self.animation_max:
            next_value = 0
        self.Set_Frame(next_value)