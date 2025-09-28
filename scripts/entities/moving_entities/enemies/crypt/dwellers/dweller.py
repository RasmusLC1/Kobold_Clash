from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys

class Dweller(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, size = (32, 32)):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, keys.dweller, size)
        self.animation_handler.Set_Animation_Num_Max(4)
        self.animation_handler.Set_Attack_Animation_Num_Max(5)

        # Dwellers get increased strength in dark
        self.light_level_holder = 999
        self.light_strength = self.strength
        self.dark_strength = self.strength * 2

        self.light_speed = self.max_speed_holder
        self.dark_speed = self.max_speed_holder * 2

        self.attack_strategy = keys.direct
        self.intent_manager.Set_Intent([keys.attack])
        self.Equip_Weapon(Claw(game, self.pos)) 

    def Update(self, tilemap, delta_time, movement=(0, 0)):
        super().Update(tilemap, delta_time, movement)
        self.Darkness_Buff()


    def Darkness_Buff(self):
        threshold = 150
        # Only run if light level crossed the threshold
        if (self.light_level < threshold) != (self.light_level_holder < threshold):
            if self.light_level < threshold:
                self.strength = self.dark_strength
                self.max_speed = self.dark_speed * 2
            else:
                self.strength = self.light_strength
                self.max_speed_holder = self.light_speed

            self.Set_Description()

        self.light_level_holder = self.light_level

    


    def Equip_Weapon(self, weapon):
        if not weapon:
            return False

        weapon.Pickup_Reset_Weapon(self)
        weapon.Set_Equip(True, self)
        self.Set_Active_Weapon(weapon)

        self.active_weapon.render = False
        del(weapon)
        return True
    
    def Spawn_Damaged_Particles(self):
        self.game.particle_handler.Activate_Particles(10, keys.bone_particle, self.rect().center)
