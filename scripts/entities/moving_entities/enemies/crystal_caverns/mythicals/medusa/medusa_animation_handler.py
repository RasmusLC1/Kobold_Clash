from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.engine.keys.keys import keys

class Medusa_Animation_Handler(Animation_Handler):

    def Set_Animation(self, action):

        if action == keys.attack:
            if self.entity.attack_type == keys.range:
                action += '_ranged'
            else:
                action += '_direct'

        super().Set_Animation(action)