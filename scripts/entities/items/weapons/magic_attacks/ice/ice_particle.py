from scripts.entities.items.weapons.magic_attacks.base_attacks.particle import Particle
from scripts.engine.assets.keys import keys


class Ice_Particle(Particle):
    def __init__(self, game, pos, shoot_distance):
        super().__init__(game, pos, keys.ice_particle_attack, 2, 1.2, 240, 100, keys.frozen, shoot_distance)
   

    def Set_Enabled(self, pos, speed, special_attack, direction, entity, delete_countdown, damage):
        self.shoot_distance = 100
        return super().Set_Enabled(pos, speed, special_attack, direction, entity, delete_countdown, damage)