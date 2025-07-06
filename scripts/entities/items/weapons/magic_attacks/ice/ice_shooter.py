from scripts.entities.items.weapons.magic_attacks.ice.ice_particle import Ice_Particle
from scripts.entities.items.weapons.magic_attacks.base_attacks.particle_shooter import Particle_Shooter
import math
from scripts.engine.keys.keys import keys

class Ice_Shooter(Particle_Shooter):
    def __init__(self, game):
        super().__init__(game)
        self.ice_cooldown = 0

    def Particle_Creation(self, entity, special_attack, damage):
        # Handle cooldown for spacing between fire particles
        if self.ice_cooldown:
            self.ice_cooldown -= 1
            return special_attack
        else:
            # Increment the special attack and set cooldown to create distance between shots
            self.ice_cooldown = 3
            special_attack = max(0, special_attack - 20)
            if not special_attack:
                return 0
            
        self.Shoot_Particles(entity, damage)
        return special_attack
    
    def Shoot_Particles(self, entity, damage, direction = None):
        
        ice_particle = self.Find_Particle()

        if not ice_particle:
            ice_particle = self.Create_Extra_Particle()
        
        speed = 1.2
        
        if not direction:
            # Calculate the base angle using atan2(y, x)
            base_angle = math.atan2(entity.attack_direction[1], entity.attack_direction[0])

            pos_x = math.cos(base_angle) * speed
            pos_y = math.sin(base_angle) * speed
            direction = (pos_x, pos_y)

        ice_particle.Set_Enabled(entity.rect(), speed, 100, direction, entity, 100, damage)
        
    
    # Append extra fire particle to the pool in case it runs out
    def Create_Extra_Particle(self):
        ice_particle = Ice_Particle(
                self.game,
                (-999, -999),
                100
            )
        self.particle_pool.append(ice_particle)
        return ice_particle
