from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
import random
from scripts.engine.assets.keys import keys

class Void_Spawn(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, size = (32, 32)):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, keys.void_spawn, size)
        self.animation_handler.Set_Animation_Num_Max(4)
        self.animation_handler.Set_Attack_Animation_Num_Max(5)
        self.Equip_Weapon(Claw(game, self.pos)) 

    def Update(self, tilemap, movement=(0, 0)):
        super().Update(tilemap, movement)
        self.Update_Active_Weapon()
        self.Weapon_Cooldown()

  
    def Set_Action(self,  movement = None):
        pass

    # Returns true on succesful attack
    def Attack(self):
        if not super().Attack():
            return False
        
        if not self.active_weapon:
            return False

        self.charge = min(self.max_weapon_charge, self.charge + 1)

        if self.charge < self.max_weapon_charge:
            return False
        
        self.Set_Target(self.game.player.pos)
        self.active_weapon.Set_Attack()
        self.Reset_Charge()
        return True

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
        self.game.particle_handler.Activate_Particles(10, keys.bone_particle, self.rect().center, frame=random.randint(10, 30))

    
    def Update_Active_Weapon(self, offset=(0, 0)):
        if not self.active_weapon:
            return

        self.active_weapon.Set_Equipped_Position(self.direction_y_holder)
        # self.active_weapon.Update(offset)
        if not self.active_weapon:
            return
        
        self.active_weapon.Update_Attack()


        return