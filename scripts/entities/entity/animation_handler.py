class Base_Animation_Handler:
    def __init__(self, entity):
        self.entity = entity
        self.sprite = None
        self.animation_value = 0

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
            self.entity.entity_image = self.sprite[self.animation_value].convert_alpha()
            self.entity.render_needs_update = True
        except Exception as e:
            print(f'Set entity image failed: {e}', self.entity.type, self.animation_value, self.sprite)

    def Set_Frame(self, value, max_value=None):
        if max_value is not None:
            value = min(value, max_value)
        self.animation_value = value
        self.Set_Entity_Image()

    def Increase_Frame(self, max_value):
        next_value = self.animation_value + 1
        if next_value > max_value:
            next_value = 0
        self.Set_Frame(next_value)