from scripts.entities.items.weapons.projectiles.projectile import Projectile
from scripts.engine.keys.keys import keys

class Spear(Projectile):
    def __init__(self, game, pos, damage_type = 'slash'):
        super().__init__(game, pos, keys.spear, 3, 6, 8, 50, 'two_handed_melee', damage_type, 30, keys.stab)
        self.max_animation = 3
        self.attack_animation_max = 3
        self.distance_from_player = 0
        
    
    # TODO: ITEM IS NOT REMOVED FROM INVENTORY SLOT
    def Shoot(self):
        self.Initialise_Shooting(self.entity_strength)

        super().Shoot()

    def Special_Attack(self):
        if not self.special_attack or not self.equipped:
            return
        self.Drop_Weapon_After_Shot()

    def Update_Attack_Animation(self):
        super().Update_Attack_Animation()




