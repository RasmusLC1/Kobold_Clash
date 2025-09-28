from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
import random
from scripts.engine.keys.keys import keys

class Void_Spawn(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, soul_value, size = (32, 32)):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, keys.void_spawn, soul_value, size)
        self.animation_handler.Set_Animation_Num_Max(4)
        self.animation_handler.Set_Attack_Animation_Num_Max(5)
        self.path_finding_strategy = keys.void_spawn
        self.attack_strategy = keys.direct
        self.intent_manager.Set_Intent([keys.attack])
        self.Equip_Weapon(Claw(game, self.pos)) 

    def Tile_Map_Collision_Detection(self, tilemap):
        self.pos[0] += self.frame_movement[0]
        self.pos[1] += self.frame_movement[1]


    # Void spawn cannot be damaged by material damage
    def Damage_Taken(self, damage, effect= (keys.slash, 0), direction = (0, 0)):
        if effect[0] == keys.slash or effect[0] == keys.blunt:
            damage = 0
        
        return super().Damage_Taken(damage, effect, direction)

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

    def Spawn_Bones(self):
        pass

