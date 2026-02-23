from scripts.entities.items.weapons.magic_attacks.poison.poison_cloud import Poison_Cloud
from scripts.entities.items.weapons.magic_attacks.base_attacks.particle_shooter import Particle_Shooter
import math
from scripts.engine.keys.keys import keys

class Poison_CLoud_Shooter(Particle_Shooter):
    def __init__(self, game):
        super().__init__(game, cooldown_max=0.6)


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
            poison_particle = self.Find_Particle()

            if not poison_particle:
                poison_particle = self.Create_Extra_Particle()
            
            angle = start_angle + j * math.radians(angle_increment)
            pos_x = math.cos(angle) * speed
            pos_y = math.sin(angle) * speed
            
            poison_particle.Set_Enabled(entity.rect(), speed, special_attack,  entity, 50, damage + self.base_damage)

    
    # Append extra fire particle to the pool in case it runs out
    def Create_Extra_Particle(self):
        fire_particle = Poison_Cloud(
                self.game,
                (-999, -999),
                2
            )
        self.particle_pool.append(fire_particle)
        return fire_particle


