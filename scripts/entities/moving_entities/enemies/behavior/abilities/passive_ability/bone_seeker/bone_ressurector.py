# scripts/entities/moving_entities/enemies/behavior/abilities/passive_ability/bone_resurrector.py
import random
from scripts.engine.keys.keys import keys
from .bone_seeker import Bone_Seeker
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability


@register_ability(keys.bone_ressurector) # add ability to registry
class Bone_Resurrector(Bone_Seeker):
    def Consume_Bones(self):
        self.game.particle_handler.Activate_Particles(10, keys.vampire_particle, self.entity.rect().center)
        self.target_bones.Revive()
        self.target_bones = None
        self.bones_search_cooldown = random.randint(25, 30)