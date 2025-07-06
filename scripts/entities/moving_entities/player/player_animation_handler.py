from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.engine.keys.keys import keys

class Player_Animation_Handler(Animation_Handler):

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
