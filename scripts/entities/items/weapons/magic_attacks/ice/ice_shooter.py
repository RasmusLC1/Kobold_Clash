from scripts.entities.items.weapons.magic_attacks.ice.ice_particle import Ice_Particle
from scripts.entities.items.weapons.magic_attacks.base_attacks.particle_shooter import Particle_Shooter
import math
from scripts.engine.keys.keys import keys

class Ice_Shooter(Particle_Shooter):
    def __init__(self, game):
        super().__init__(game, cooldown_max=0.3)
        self.range = 100
        self.speed = 1.2


    def Shoot_Particles(self):
        
        ice_particle = self.Find_Particle()

        if not ice_particle:
            ice_particle = self.Create_Extra_Particle()
        

        self.entity.Set_Attack_Direction()

    
        # Calculate the base angle using atan2(y, x)
        base_angle = math.atan2(self.entity.attack_direction[1], self.entity.attack_direction[0])

        pos_x = math.cos(base_angle) * self.speed
        pos_y = math.sin(base_angle) * self.speed
        direction = (pos_x, pos_y)

        ice_particle.Set_Enabled(self.entity.rect(), self.speed, self.range, direction, self.entity, 100, self.base_damage)
        
    
    # Append extra fire particle to the pool in case it runs out
    def Create_Extra_Particle(self):
        ice_particle = Ice_Particle(
                self.game,
                (-999, -999),
                100
            )
        self.particle_pool.append(ice_particle)
        return ice_particle
