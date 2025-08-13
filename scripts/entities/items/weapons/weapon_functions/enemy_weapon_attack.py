import random
from scripts.engine.keys.keys import keys

class Enemy_Weapon_Attack():
    def __init__(self, game, weapon):
        self.game = game
        self.weapon = weapon
        self.player_hit_effect_cooldown = 0
        
        self.attacking = 0


    # Update the attack logic
    def Update_Attack(self, delta_time):

        self.Update_Player_Hit_Effect_Cooldown(delta_time)

        if not self.attacking:
            return False

        self.attacking -= delta_time


        self.weapon.entity.Reduce_Movement(4) # Reduce movement to a quarter when attacking
        return False
    
    # Initialise the attack and reset attack values
    def Set_Attack(self):
        if not self.Check_Entity_Cooldown():
            return
        entity = self.weapon.entity
        # self.attacking = max(int((self.weapon.speed) // entity.agility), self.weapon.attack_animation_max)
        self.attacking = max(0.1, 4 - (self.weapon.speed + entity.agility) / 10)

        self.attack_animation_time = int(self.attacking / self.weapon.attack_animation_max)
        if entity.distance_to_player > self.game.tilemap.tile_size * 1.5:
            return
        self.weapon.Entity_Hit(self.game.player)
        self.Set_player_Hit_Effect()

    def Reset_Attack(self):
        if not self.attacking <= 1:
            return False
        
        self.attacking = 0
        self.weapon.Reset_Attack_Animation()

        return True
        
    # Return False if entity weapon cooldown is not off
    def Check_Entity_Cooldown(self):
        if self.weapon.entity.active_weapon_cooldown:
            return False
        return True
    
        # Cooldown function to prevent constant screenshake and freezeframes
    def Update_Player_Hit_Effect_Cooldown(self, delta_time):
        if not self.player_hit_effect_cooldown > 0:
            return
        self.player_hit_effect_cooldown -= delta_time

    def Set_player_Hit_Effect(self):
        if self.player_hit_effect_cooldown > 0:
            return
        

        damage = self.weapon.damage_handler.Get_Damage()
        damage_freeze = max(10, min(30, damage // 5))
        self.game.logic_update.Set_Freeze_Frame(damage_freeze)

        self.game.camera_update.Set_Screen_Shake(damage_freeze, damage_freeze // 2)
        self.player_hit_effect_cooldown = 0.3
        self.game.sound_handler.Play_Sound(keys.player_hit, 0.3)
        self.game.particle_handler.Activate_Particles(random.randint(10, 20), keys.player_particle, self.game.player.rect().center)



