from scripts.engine.keys.keys import keys
import random

class Noise():
    def __init__(self, game):
        self.timer = 0
        self.pos = None
        self.sprite = game.assets[keys.noise]

    def Set_Active(self, pos):
        self.pos = pos
        self.timer = random.randint(90, 100)
        # Set a random variant
        variant = random.randint(0, 2)
        self.image = self.sprite[variant]

    def Update(self):
        self.timer -= 1
        self.pos[1] -= 0.2

        if not self.timer:
            return False
        
        return True

    def Render(self, surf, offset):
        if self.timer < 60: 
            self.image.set_alpha(self.timer * 2)
        surf.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
