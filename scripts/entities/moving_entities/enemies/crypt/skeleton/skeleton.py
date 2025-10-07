from scripts.entities.moving_entities.enemies.enemy import Enemy
import random
from scripts.engine.keys.keys import keys

class Skeleton(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, soul_value, size = (32, 32)):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, keys.skeleton, soul_value, size)
        self.animation_handler.Set_Animation_Num_Max(6)
        self.animation_handler.Set_Attack_Animation_Num_Max(6)

    def Set_Action(self,  movement = None):
        if self.charge:
            self.animation_handler.Set_Animation(keys.attack)
        else:
            self.animation_handler.Set_Animation('running')


    def Spawn_Damaged_Particles(self):
        self.game.particle_handler.Activate_Particles(10, keys.bone_particle, self.rect().center)

