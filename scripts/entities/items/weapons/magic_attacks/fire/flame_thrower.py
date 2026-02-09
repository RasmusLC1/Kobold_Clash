from scripts.entities.items.weapons.magic_attacks.fire.fire_particle import Fire_Particle
from scripts.entities.items.weapons.magic_attacks.base_attacks.particle_shooter import Particle_Shooter
import math

class Flame_Thrower(Particle_Shooter):
    def __init__(self, game):
        super().__init__(game, range=40, speed=1, cooldown_max=0.5, particle_type=Fire_Particle)


    def Shoot_Particles(self):
        # Basic raycasting attributes
        num_lines = 8  # Define the number of lines and the spread angle (in degrees)
        spread_angle = 50  # Total spread of the fan (in degrees)
        angle_increment = spread_angle / (num_lines - 1)  # Calculate the angle increment between each line
        entity = self.entity
        # Calculate the base angle using atan2(y, x)
        self.entity.Set_Attack_Direction()
        base_angle = math.atan2(entity.attack_direction[1], entity.attack_direction[0])
        start_angle = base_angle - math.radians(spread_angle / 2)


        # Generate fire particles
        for j in range(num_lines):
            fire_particle = self.Find_Particle()

            if not fire_particle:
                fire_particle = self.Create_Extra_Particle()
            
            angle = start_angle + j * math.radians(angle_increment)
            pos_x = math.cos(angle) * self.speed
            pos_y = math.sin(angle) * self.speed
            direction = (pos_x, pos_y)
            
            fire_particle.Set_Enabled(entity.rect(), self.speed, self.range, direction, entity, 50, self.base_damage)


