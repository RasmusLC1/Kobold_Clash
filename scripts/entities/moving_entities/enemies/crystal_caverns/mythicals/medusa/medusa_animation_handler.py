from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.engine.keys.keys import keys

class Medusa_Animation_Handler(Animation_Handler):

    def Set_Animation(self, action):
        super().Set_Animation(action)

        if action != keys.attack:
            return
        
        if self.entity.attack_type == keys.range:
            self.animation = keys.medusa_attack_ranged
        else:
            self.animation = keys.medusa_attack_direct