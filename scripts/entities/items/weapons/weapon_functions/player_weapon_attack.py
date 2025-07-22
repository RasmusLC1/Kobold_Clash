import pygame
from scripts.engine.keys.keys import keys

class Player_Weapon_Attack():
    def __init__(self, game, weapon):
        self.game = game
        self.weapon = weapon
        
        self.ready_to_delete = False
        self.attacking = 0
        self.attack_hitbox_size = (10, 10)
        self.attack_hitbox = pygame.Rect(self.weapon.pos[0], self.weapon.pos[1], self.attack_hitbox_size[0], self.attack_hitbox_size[1])
        self.entities_hit = [] # Enemies which have been hit by an attack
        self.nearby_enemies = [] # Nearby enemies that the weapon can interact with
        self.nearby_decoration = [] # Nearby decoration that the weapon can interact with
        self.player = self.game.player
        self.enemy_hit_effect_cooldown = 0
        self.active = False

    # Update the attack logic
    def Update_Attack(self, delta_time):
        self.Update_Enemy_Hit_Effect_Cooldown(delta_time)
        if self.attacking < 0:
            return False
        entity = self.Attack_Collision_Check()
        self.attacking -= delta_time
        if self.attacking <= 0:
            self.active = False
        return self.ready_to_delete


    # Initialise the attack and reset attack values
    def Set_Attack(self):
        if not self.Check_Entity_Cooldown():
            return False
        self.Reset_Entities_Hit()
        self.player.Attack_Direction_Handler()
        
        # Compute attack each time to account for changing player agility level
        self.Set_Attacking()
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.player, 3) # Find nearby enemies to attack
        self.nearby_decoration = self.game.decoration_handler.Find_Nearby_Decorations(self.player.pos, 3)
        return True
    
    def Attack_Collision_Check(self):
        self.Set_Attack_Hitbox()

        if not self.weapon.Check_Tile(self.attack_hitbox.center):
            self.Reset_Attack()

        enemy_hit = self.Enemy_Collision()        
        if enemy_hit:
            self.Set_Enemy_Hit_Effect()
            return enemy_hit
        return self.Decoration_Collision()
    

    def Enemy_Collision(self):
        for enemy in self.nearby_enemies:
            # Prevent from hitting enemy multiple times
            if enemy in self.entities_hit:
                continue
            # Check for collision with enemy
            if self.attack_hitbox.colliderect(enemy.rect()):
                self.weapon.Entity_Hit(enemy)
                self.entities_hit.append(enemy)

                self.Check_Durability(1)
                

                # Return enemy in case further effects need to be added such as knockback
                return enemy
            
        return None
    
    # Subtracts durability and sets flag for if the weapon needs to be deleted
    def Check_Durability(self, damage):
        self.weapon.Decrease_Durability(damage)

        if self.weapon.durability <= 0:
            self.game.sound_handler.Play_Sound('weapon_break', 0.5)
            self.ready_to_delete = True

        return

    def Decoration_Collision(self):
        for decoration in self.nearby_decoration:
            # Check if the decoration can be damaged
            if not decoration.destructable:
                continue
            # Prevent from hitting decoration multiple times
            if decoration in self.entities_hit:
                continue
            # Check for collision with enemy
            if self.attack_hitbox.colliderect(decoration.rect()):
                self.weapon.Decoration_Hit(decoration)
                self.Check_Durability(2)
                self.entities_hit.append(decoration)
                return decoration
        
        return None
    
        # Return False if player weapon cooldown is not off
    def Check_Entity_Cooldown(self):
        if self.player.active_weapon_cooldown:
            return False
        return True

    def Reset_Attack(self):
        
        if self.attacking > 0:
            return False
        self.attacking = 0
        self.active = False
        self.weapon.Reset_Attack_Animation()
        self.player.Reset_Attack_Direction()

        return True
    
    # Compute the hitbox for the weapon when attacking
    def Set_Attack_Hitbox(self):
        if not self.player:
            return
        pos_x = self.weapon.rect().center[0] - 2 + self.player.attack_direction[0] * self.game.tilemap.tile_size
        pos_y = self.weapon.rect().center[1] - 2 + self.player.attack_direction[1] * self.game.tilemap.tile_size
        self.attack_hitbox = pygame.Rect(pos_x, pos_y, self.attack_hitbox_size[0] * self.weapon.range, self.attack_hitbox_size[1] * self.weapon.range)

    def Reset_Entities_Hit(self):
        self.entities_hit.clear()

        
    # Cooldown function to prevent constant screenshake and freezeframes
    def Update_Enemy_Hit_Effect_Cooldown(self, delta_time):
        if not self.enemy_hit_effect_cooldown:
            return
        self.enemy_hit_effect_cooldown -= delta_time

    def Set_Attacking(self):
        self.attacking = max(0.1, 2 - (self.weapon.speed + self.player.agility) / 10)

    def Set_Enemy_Hit_Effect(self):
        if self.enemy_hit_effect_cooldown > 0:
            return
        

        damage = self.weapon.damage_handler.Get_Damage()
        damage_freeze = max(5, min(20, damage // 10))
        self.game.logic_update.Set_Freeze_Frame(damage_freeze)

        self.game.camera_update.Set_Screen_Shake(damage_freeze, damage_freeze // 2)
        self.enemy_hit_effect_cooldown = 1
        self.game.sound_handler.Play_Sound('enemy_hit', 0.3)

