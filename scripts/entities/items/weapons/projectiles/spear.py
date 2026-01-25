from scripts.entities.items.weapons.projectiles.projectile import Projectile
from scripts.engine.keys.keys import keys

class Spear(Projectile):
    def __init__(self, game, pos, damage_type = 'slash'):
        super().__init__(game, pos, type=keys.spear, damage=3, speed=6, range=8, max_charge_time=50, weapon_class='two_handed_melee', effect=damage_type, shoot_distance=30, attack_types=[keys.stab], max_animation=0, max_amount=1)
        self.distance_from_player = 0
        
    
    # TODO: ITEM IS NOT REMOVED FROM INVENTORY SLOT
    def Shoot(self, delta_time):
        if not self.shoot_speed:
            self.Initialise_Shooting(self.entity_strength)

        super().Shoot(delta_time)

    def Special_Attack(self):
        if not self.special_attack or not self.equipped:
            return
        self.Drop_Weapon_After_Shot()

    def Update_Attack_Animation(self):
        super().Update_Attack_Animation()




