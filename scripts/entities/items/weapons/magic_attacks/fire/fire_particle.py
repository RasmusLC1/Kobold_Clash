from scripts.entities.items.weapons.magic_attacks.base_attacks.particle import Particle
from scripts.engine.keys.keys import keys


class Fire_Particle(Particle):
    def __init__(self, game, pos, shoot_distance):
        super().__init__(game, pos, keys.fire_particle_attack, 2, 1, 2, 100, keys.fire, shoot_distance)
