# scripts/entities/moving_entities/enemies/behavior/abilities/passive_ability/bone_resurrector.py
import random
from scripts.engine.keys.keys import keys
from .bone_seeker import Bone_Seeker

class Bone_Resurrector(Bone_Seeker):
    def Consume_Bones(self):
        self.game.particle_handler.Activate_Particles(10, keys.vampire_particle, self.entity.rect().center)
        self.target_bones.Revive()
        self.target_bones = None
        self.bones_search_cooldown = random.randint(25, 30)