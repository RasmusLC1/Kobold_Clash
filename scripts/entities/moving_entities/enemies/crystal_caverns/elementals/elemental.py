from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.engine.keys.keys import keys

ICE_PROJECTILE_NUM = 3 * 20
CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX = 1 # heals 1 health every second

class Elemental(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, soul_value):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, keys.elemental, soul_value)
        self.crystal_scale_max = self.max_health // 2
        self.crystal_scale = self.crystal_scale_max
        self.crystal_scale_heal_cooldown = CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        if not super().Update(tilemap, delta_time, movement):
            return False
        self.Heal_Crystal_Scale(delta_time)
        return True
        
    
    def Heal_Crystal_Scale(self, delta_time):
        if self.crystal_scale == self.crystal_scale_max:
            return
        
        if self.crystal_scale_heal_cooldown <= 0:
            self.crystal_scale = min(self.crystal_scale + 1, self.crystal_scale_max)
            self.crystal_scale_heal_cooldown = CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX
            return
        
        self.crystal_scale_heal_cooldown -= delta_time


    def Damage_Taken(self, damage, effect = (keys.slash, 0), direction = (0, 0)):
        if self.crystal_scale > 0:
            absorbed = min(damage, self.crystal_scale)
            damage -= absorbed
            self.crystal_scale -= absorbed
        if damage > 0:
            return super().Damage_Taken(damage, effect, direction)
        return True

        




    def Render_Weapons(self, surf, offset):
        pass