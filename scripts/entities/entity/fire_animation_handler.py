from .base_animation_handler import Base_Animation_Handler
import random

class Fire_Animation_Handler(Base_Animation_Handler):
    def Increase_Frame(self):
        next_value = random.randint(1, self.animation_max)
        self.Set_Frame(next_value)
