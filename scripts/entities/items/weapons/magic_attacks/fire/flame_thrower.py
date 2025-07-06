from scripts.entities.items.weapons.magic_attacks.fire.fire_particle import Fire_Particle
from scripts.entities.items.weapons.magic_attacks.base_attacks.particle_shooter import Particle_Shooter
import math
from scripts.engine.keys.keys import keys

class Flame_Thrower(Particle_Shooter):
    def __init__(self, game):
        super().__init__(game)
        self.fire_cooldown = 0

    def Particle_Creation(self, entity, special_attack, damage):
        if self.fire_cooldown:
            self.fire_cooldown -= 1
            return special_attack
        else:
            self.fire_cooldown = 3
            special_attack = max(0, special_attack - 20)
            if special_attack <= 0:
                return 0
            
        self.Shoot_Particles(entity, special_attack, damage)
        return special_attack


    def Shoot_Particles(self, entity, special_attack, damage):
        # Basic raycasting attributes
        num_lines = 8  # Define the number of lines and the spread angle (in degrees)
        spread_angle = 50  # Total spread of the fan (in degrees)
        angle_increment = spread_angle / (num_lines - 1)  # Calculate the angle increment between each line

        # Calculate the base angle using atan2(y, x)
        base_angle = math.atan2(entity.attack_direction[1], entity.attack_direction[0])
        start_angle = base_angle - math.radians(spread_angle / 2)

        speed = 1  

        # Generate fire particles
        for j in range(num_lines):
            fire_particle = self.Find_Particle()

            if not fire_particle:
                fire_particle = self.Create_Extra_Particle()
            
            angle = start_angle + j * math.radians(angle_increment)
            pos_x = math.cos(angle) * speed
            pos_y = math.sin(angle) * speed
            direction = (pos_x, pos_y)
            
            fire_particle.Set_Enabled(entity.rect(), speed, special_attack, direction, entity, 50, damage)

    
    # Append extra fire particle to the pool in case it runs out
    def Create_Extra_Particle(self):
        fire_particle = Fire_Particle(
                self.game,
                (-999, -999),
                100
            )
        self.particle_pool.append(fire_particle)
        return fire_particle


