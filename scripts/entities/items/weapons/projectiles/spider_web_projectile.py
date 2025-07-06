from scripts.entities.items.weapons.projectiles.projectile import Projectile
from scripts.engine.keys.keys import keys

class Spider_Web_Projectile(Projectile):
    def __init__(self, game, pos, type, damage, speed, shoot_distance, weapon_class, special_attack, direction, entity):
        super().__init__(game, pos, type, damage, speed, 2, 40, weapon_class, keys.blunt, shoot_distance, keys.cut, (5, 5), False)
        self.special_attack = special_attack
        self.entity = entity
        self.attack_direction = direction  # Store the direction vector
        self.target_hit = 0
        self.delete_countdown = 100
        self.pickup_allowed = False
        self.attack_animation_max = 3
        self.attack_animation_time = shoot_distance // self.attack_animation_max

    def Update_Text_Box(self, hitbox_1, hitbox_2):
        pass

    def Shoot(self):
        if not self.shoot_speed:
            self.Initialise_Shooting(self.speed)
        if self.target_hit:
            self.target_hit -= 1
            if not self.target_hit:
                self.Set_Special_Attack(0)
            return

        entity = super().Shoot()
        self.Entity_Collision_Detection(entity)

    def Entity_Collision_Detection(self, entity):
        # entity = self.Attack_Collision_Check_Projectile()
        if entity:
            entity.Set_Effect(keys.snare, 3)
            self.animation = self.attack_animation_max
            self.pos = entity.pos
            return True
        
        return False


    def Reset_Shot(self):
        self.target_hit = 100
        self.delete_countdown = 100
        
