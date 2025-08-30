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
        self.crystal_scale_bar = self.game.assets[keys.crystal_scale_bar]

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

        
    def Render_Health_Bar(self, surf, offset = (0,0)):
        super().Render_Health_Bar(surf, offset)
        self.Render_Crystal_Scale_Bar(surf, offset)
    
    def Render_Crystal_Scale_Bar(self, surf, offset):
        if not self.crystal_scale:
            return
        crystal_scale_fraction = self.crystal_scale / self.crystal_scale_max

        # Map the fraction to an index from 0 to 9 (assuming 10 total images)
        crystal_scale_index = max(-1, min(int((1 - crystal_scale_fraction) * 9), 9))  # Invert fraction and scale to index range
        # Correct potential rounding issues at full health
        if self.crystal_scale == self.crystal_scale_max:
            crystal_scale_index = 0

        crystal_scale_bar = self.crystal_scale_bar[crystal_scale_index]
        surf.blit(crystal_scale_bar, (self.rect().left - offset[0], self.rect().bottom - offset[1] - self.size[1] // 2 + 10))


    def Render_Weapons(self, surf, offset):
        pass