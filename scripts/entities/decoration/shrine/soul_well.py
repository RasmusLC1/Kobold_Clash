from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys
import math


class Soul_Well(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.soul_well, pos, (64, 64))
        self.description = "sacrifice gold\nfor souls"
        self.animation_cooldown = 0
        self.max_animation = 3



    def Update(self):
        self.Update_Animation()
        return super().Update()

    def Update_Animation(self):
        if not self.animation_cooldown_Handler():
            return
        
        if self.animation >= self.max_animation:
            self.Set_Animation(0)
        else:
            self.Set_Animation(self.animation + 1)
        spawn_particles = random.randint(0, 4)
        if spawn_particles == 0:
            self.game.particle_handler.Activate_Particles(random.randint(2, 4), keys.soul_particle, self.rect().center, frame=random.randint(50, 70))


    def animation_cooldown_Handler(self):
        if self.animation_cooldown <= 0:
            self.animation_cooldown = random.randint(40, 60)
            return True
        
        self.animation_cooldown -= 1
        return False


    def Spawn_Reward(self, item):
        self.game.player.Set_Last_Shrine(self)
        self.game.player.Increase_Souls(item.amount * item.value * 2)
        self.game.item_handler.Remove_Item(item, True)
        self.game.particle_handler.Activate_Particles(random.randint(8, 12), keys.soul_particle, self.rect().center, frame=random.randint(50, 70))
        
        self.Generate_Sound('soul_well', 0.6, 1000)

        return True
