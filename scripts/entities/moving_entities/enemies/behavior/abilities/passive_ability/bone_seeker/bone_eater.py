import random
from scripts.engine.keys.keys import keys
from .bone_seeker import Bone_Seeker
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability


@register_ability(keys.bone_eater) # add ability to registry
class Bone_Eater(Bone_Seeker):
    def Consume_Bones(self):
        self.game.particle_handler.Activate_Particles(10, keys.vampire_particle, self.entity.rect().center)
        self.entity.effects.Set_Effect(keys.healing, self.entity.max_health // 2)
        self.target_bones.Consume()
        self.target_bones = None
        self.bones_search_cooldown = random.randint(25, 30)