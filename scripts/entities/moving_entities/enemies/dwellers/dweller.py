from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
import random
from scripts.engine.assets.keys import keys
import math

class Dweller(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, size = (32, 32)):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, max_weapon_charge, keys.dweller, size)
        self.animation_handler.Set_Animation_Num_Max(4)
        self.animation_handler.Set_Attack_Animation_Num_Max(5)
        self.seek_darkness_cooldown = 0
        self.light_counter = 0
        self.attack_strategy = 'direct'
        self.intent_manager.Set_Intent(['attack'])
        self.Equip_Weapon(Claw(game, self.pos)) 

    def Update(self, tilemap, movement=(0, 0)):
        super().Update(tilemap, movement)
        self.Update_Active_Weapon()
        self.Weapon_Cooldown()
        self.Darkness_Counter_Handler()


    # Dwellers avoid light and prefer to stay in dark
    def Darkness_Counter_Handler(self):
        if self.distance_to_player > 200:
            return
        
        if self.seek_darkness_cooldown:
            self.seek_darkness_cooldown -= 1
            return

        if self.light_level < 2:
            self.light_counter = 0
            return
        
        if self.light_level >= 2:
            self.light_counter += 1

            if self.light_counter > 300:
                fail = 0
                while fail < 4:
                    tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
                    tile_distance = math.sqrt((tile.pos[0] - self.game.player.pos[0]) ** 2 + (tile.pos[1] - self.game.player.pos[1]) ** 2)
                    if tile_distance > 200:
                        break
                    fail += 1
                    if fail > 3:
                        return
                
                self.game.enemy_handler.Add_To_Pathfinding_Queue(self, tile.pos)
                self.seek_darkness_cooldown = 2000
                self.Set_Action('run_away')
                print("SEEK DARKNESS", self.distance_to_player, self.target, self.game.player.pos)

        



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
        if not self.active_weapon:
            return
        
        self.active_weapon.Update_Attack()


        return