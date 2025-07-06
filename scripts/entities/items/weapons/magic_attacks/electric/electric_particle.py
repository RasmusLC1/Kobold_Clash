from scripts.entities.items.weapons.magic_attacks.base_attacks.particle import Particle
from scripts.engine.keys.keys import keys


class Electric_Particle(Particle):
    def __init__(self, game, pos, shoot_distance):
        super().__init__(game, pos, keys.electric_particle_attack, 2, 2, 1, 100, keys.electric, shoot_distance)
    
 
    

