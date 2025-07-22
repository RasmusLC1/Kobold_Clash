from scripts.entities.moving_entities.enemies.crypt.dwellers.dweller import Dweller
from scripts.engine.keys.keys import keys

import random

# TODO: Implement intent with spider and make attacks into objects
class Ghoul(Dweller):

    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.ghoul, health, strength, max_speed, agility, intelligence, stamina, 0.8, 15)

        self.intent_manager.Set_Intent([keys.direct, keys.attack, keys.attack, keys.attack, keys.medium_range])

        self.animation_handler.Set_Animation_Num_Max(4)
        self.animation_handler.Set_Attack_Animation_Num_Max(5)
        self.bones_search_cooldown = 0
        self.target_bones_collision_cooldown = 0
        self.target_bones = None


        self.attack_symbol_offset = 10
        self.active_weapon.Set_Damage(keys.poison, 2)
        self.active_weapon.Set_Damage(keys.blunt, 3)

    
    def Update(self, tilemap, delta_time, movement=(0, 0)):
        self.Update_Bones_Search_Cooldown(delta_time)
        self.Search_For_Bones()
        self.Bones_Collision_Check()
        super().Update(tilemap, delta_time, movement)
        

    def Update_Bones_Search_Cooldown(self, delta_time):
        if not self.bones_search_cooldown:
            return
        
        self.bones_search_cooldown = max(0, self.bones_search_cooldown - delta_time)

    def Bones_Collision_Check(self):
        if not self.target_bones:
            return
        if self.target_bones_collision_cooldown:
            self.target_bones_collision_cooldown = max(0, self.target_bones_collision_cooldown - 1)
            return
        else:
            self.target_bones_collision_cooldown = 50
            self.Heal_From_Bones()

    def Heal_From_Bones(self):
        if self.target_bones and self.rect().colliderect(self.target_bones.rect()):
            self.game.particle_handler.Activate_Particles(10, keys.vampire_particle, self.rect().center)
            self.bones_search_cooldown = random.randint(25, 30)
            self.effects.Set_Effect(keys.healing, self.max_health // 2)
            return

    def Search_For_Bones(self):
        if self.bones_search_cooldown:
            return
        # self.bones_search_cooldown = random.randint(900, 1100)
        self.bones_search_cooldown = random.randint(2, 4)
        nearby_bones = self.game.tilemap.Search_Nearby_Tiles_For_Type(5, self.pos, keys.bones, self.ID)
        if not nearby_bones:
            return
            
        self.locked_on_target = False
        self.game.enemy_handler.Add_To_Pathfinding_Queue(self, nearby_bones[0].pos)
        self.Set_Attack_Strategy(keys.medium_range)
        self.target_bones = nearby_bones[0]


