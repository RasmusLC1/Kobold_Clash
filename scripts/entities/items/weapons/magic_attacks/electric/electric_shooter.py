from scripts.entities.items.weapons.magic_attacks.electric.electric_particle import Electric_Particle
from scripts.entities.items.weapons.magic_attacks.base_attacks.particle_shooter import Particle_Shooter

import math
from scripts.engine.keys.keys import keys

class Electric_Shooter(Particle_Shooter):
    def __init__(self, game):
        super().__init__(game, cooldown_max=0.4)
        self.range = 50
            
    def Shoot_Particles(self):
        speed = 2

        electric_particle = self.Find_Particle()
        self.entity.Set_Attack_Direction()


        if not electric_particle:
            electric_particle = self.Create_Extra_Particle()


        # Calculate the base angle using atan2(y, x)
        base_angle = math.atan2(self.entity.attack_direction[1], self.entity.attack_direction[0])

        pos_x = math.cos(base_angle) * speed
        pos_y = math.sin(base_angle) * speed
        direction = (pos_x, pos_y)
        electric_particle.Set_Enabled(self.entity.rect(), speed, self.range, direction, self.entity, 100, self.base_damage)
        
        
        
    # Append extra fire particle to the pool in case it runs out
    def Create_Extra_Particle(self):
        electric_particle = Electric_Particle(
                self.game,
                (-999, -999),
                100
            )
        self.particle_pool.append(electric_particle)
        return electric_particle


        