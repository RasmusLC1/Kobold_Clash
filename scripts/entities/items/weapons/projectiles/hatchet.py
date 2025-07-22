from scripts.entities.items.weapons.projectiles.projectile import Projectile
from scripts.engine.keys.keys import keys


class Hatchet(Projectile):
    def __init__(self, game, pos, damage_type = 'slash'):
        super().__init__(game, pos, keys.hatchet, 5, 3, 4, 40, 'one_handed_melee', damage_type, 20, keys.cut)
        self.max_animation = 3
        self.attack_animation_max = 3
        self.distance_from_player = 0
        
    
    def Shoot(self, delta_time):
        if not self.shoot_speed:
            self.Initialise_Shooting(self.entity_strength)
        self.rotate += 5

        super().Shoot(delta_time)

    def Special_Attack(self):
        if not self.special_attack or not self.equipped:
            return
        self.Drop_Weapon_After_Shot()

