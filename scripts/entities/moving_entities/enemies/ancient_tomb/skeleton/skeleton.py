from scripts.entities.moving_entities.enemies.enemy import Enemy
import random
from scripts.engine.keys.keys import keys

class Skeleton(Enemy):
    def __init__(self, game, pos, type):
        super().__init__(game, pos, type)

    def Set_Action(self,  movement = None):
        if self.charge:
            self.animation_handler.Set_Animation(keys.attack)
        else:
            self.animation_handler.Set_Animation('running')


    def Spawn_Damaged_Particles(self):
        self.game.particle_handler.Activate_Particles(10, keys.bone_particle, self.rect().center)

