from scripts.entities.items.weapons.magic_attacks.electric.electric_particle import Electric_Particle
from scripts.entities.items.weapons.magic_attacks.base_attacks.particle_shooter import Particle_Shooter

import math
from scripts.engine.keys.keys import keys

class Electric_Shooter(Particle_Shooter):
    def __init__(self, game):
        super().__init__(game)
        self.electric_cooldown = 0

    def Particle_Creation(self, entity, special_attack, damage):
        # Handle cooldown for spacing between fire particles
        if self.electric_cooldown:
            self.electric_cooldown -= 1
            return special_attack
        else:
            self.electric_cooldown = 9
            special_attack = max(0, special_attack - 60)
            if not special_attack:
                return 0
            
        self.Shoot_Particles(entity, special_attack, damage)
        return special_attack
            
    def Shoot_Particles(self, entity, special_attack, damage):
        speed = 2

        electric_particle = self.Find_Particle()

        if not electric_particle:
            electric_particle = self.Create_Extra_Particle()


        # Calculate the base angle using atan2(y, x)
        base_angle = math.atan2(entity.attack_direction[1], entity.attack_direction[0])

        pos_x = math.cos(base_angle) * speed
        pos_y = math.sin(base_angle) * speed
        direction = (pos_x, pos_y)
        electric_particle.Set_Enabled(entity.rect(), speed, special_attack, direction, entity, 100, damage)
        
        
        
    # Append extra fire particle to the pool in case it runs out
    def Create_Extra_Particle(self):
        electric_particle = Electric_Particle(
                self.game,
                (-999, -999),
                100
            )
        self.particle_pool.append(electric_particle)
        return electric_particle


        