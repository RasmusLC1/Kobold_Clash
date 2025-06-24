from scripts.entities.items.weapons.weapon import Weapon
from scripts.entities.items.weapons.magic_attacks.electric.electric_shooter import Electric_Shooter
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.entities.items.weapons.magic_attacks.vampiric.soul_reap_shooter import Soul_Reap_Shooter 
from scripts.engine.assets.keys import keys
import random

class Staff(Weapon):
    def __init__(self, game, pos):
        self.Set_Type()
        super().__init__(game, pos, self.sub_type, 3, 8, 10, 50, 'one_handed_melee', keys.blunt)
        self.max_animation = 0
        self.attack_animation_max = 2
        self.attack_animation_counter = 0
        self.shooter = None

    # Handle special attack charge
    def Special_Attack(self):
        if not self.entity:
            return
        
        if self.special_attack <= 0 or not self.equipped:
            return
        self.Shoot_Projectiles()
        

    # Initialise the charge logic
    def Shoot_Projectiles(self):
        if self.type == keys.fire_staff or self.type == keys.electric_staff:
            self.shooter.Shoot_Particles(self.entity, 10)
        elif self.type == keys.frozen_staff:
            self.shooter.Shoot_Particles(self.entity, self.entity.attack_direction)
        elif self.type == keys.vampiric_staff:
            self.shooter.Spawn_Soul_Reap(self.entity)
        self.special_attack = 0



    def Set_Type(self):
        types = {
            keys.electric_staff: Electric_Shooter,
            keys.fire_staff: Flame_Thrower,
            keys.frozen_staff: Ice_Shooter,
            keys.vampiric_staff: Soul_Reap_Shooter,
        }
        self.sub_type , self.shooter = random.choice(list(types.items()))

