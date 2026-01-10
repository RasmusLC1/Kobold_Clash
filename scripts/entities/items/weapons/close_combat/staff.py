from scripts.entities.items.weapons.weapon import Weapon
from scripts.entities.items.weapons.magic_attacks.electric.electric_shooter import Electric_Shooter
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.entities.items.weapons.magic_attacks.vampiric.soul_reap_shooter import Soul_Reap_Shooter 
from scripts.engine.keys.keys import keys
import random

class Staff(Weapon):
    def __init__(self, game, pos):
        self.Set_Random_Type(game)
        super().__init__(game, pos, self.sub_type, 2, 4, 7, 50, 'two_handed_melee', keys.blunt)

        self.cooldown = 0
        self.max_cooldown = 10
        self.charge_attack = 0

    def Load_Data(self, data):
        super().Load_Data(data)
        self.Set_Type(self.game)



    # Handle special attack charge
    def Special_Attack(self):
        if not self.entity:
            return
        
        if self.special_attack <= 0 or not self.equipped:
            return
        
        self.entity.Attack_Direction_Handler()
        self.Shoot_Projectiles()
        

    # Initialise the charge logic
    def Shoot_Projectiles(self):
        if not self.shooter or not self.entity:
            return

        if self.type == keys.vampiric_staff:
            self.shooter.Spawn_Soul_Reap(self.entity, self.particle_damage)
            self.special_attack = 0
        else:
            if not self.charge_attack:
                self.charge_attack = 80
            self.charge_attack = self.shooter.Particle_Creation(self.entity, self.charge_attack, self.particle_damage)
        # self.Set_Cooldown()
        # Pays a soul cost for using the staff
        if self.entity.type == keys.player and self.charge_attack <= 0:
            self.charge_attack = 0
            self.special_attack = 0
            self.game.player.Decrease_Souls(3)


    
    def Set_Cooldown(self):
        self.cooldown = self.max_cooldown

    def Set_Random_Type(self, game):
        if hasattr(self, 'sub_type'):
            return
        types = {
            keys.electric_staff: Electric_Shooter,
            keys.fire_staff: Flame_Thrower,
            keys.frozen_staff: Ice_Shooter,
            keys.vampiric_staff: Soul_Reap_Shooter,
        }
        self.sub_type, shooter_class = random.choice(list(types.items()))
        self.shooter = shooter_class(game)
        self.Set_Particle_Damage()


    def Set_Type(self, game):
        types = {
            keys.electric_staff: Electric_Shooter,
            keys.fire_staff: Flame_Thrower,
            keys.frozen_staff: Ice_Shooter,
            keys.vampiric_staff: Soul_Reap_Shooter,
        }

        shooter_class = types.get(self.sub_type)
        self.shooter = shooter_class(game)
        self.Set_Particle_Damage()        

    def Set_Particle_Damage(self):
        particle_damge = {
            keys.electric_staff: 15,
            keys.fire_staff: 5,
            keys.frozen_staff: 20,
            keys.vampiric_staff: 20,
        }
        self.particle_damage = particle_damge.get(self.sub_type)