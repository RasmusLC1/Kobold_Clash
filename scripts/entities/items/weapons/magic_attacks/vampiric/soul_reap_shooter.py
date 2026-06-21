from scripts.entities.items.weapons.magic_attacks.vampiric.soul_reap import Soul_Reap
import math
from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.magic_attacks.base_attacks.particle_shooter import Particle_Shooter


class Soul_Reap_Shooter(Particle_Shooter):
    def __init__(self, game, entity):
        super().__init__(game, entity, speed=1.4, range=100 ,cooldown_max=0.3, particle_type=Soul_Reap)

        
    
    def Shoot_Particles(self):
        # Calculate the base angle using atan2(y, x)
        base_angle = math.atan2(self.entity.attack_direction[1], self.entity.attack_direction[0])

        pos_x = math.cos(base_angle) * self.speed
        pos_y = math.sin(base_angle) * self.speed
        direction = (pos_x, pos_y)

        soul_reap = Soul_Reap(
                self.game,
                self.entity.rect(),
                self.base_damage,
                self.speed,
                self.range,
                100,
                direction,  # Pass the direction here
                self.entity
            )
        
        self.game.item_handler.Add_Item(soul_reap)

    
    # Interpreter for enemy attacks
    def Set_Attack(self):
        self.Shoot_Particles()