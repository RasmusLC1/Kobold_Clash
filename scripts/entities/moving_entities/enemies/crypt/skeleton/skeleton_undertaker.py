from scripts.entities.items.weapons.close_combat.scythe import Scythe
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.engine.keys.keys import keys

import random


class Skeleton_Undertaker(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        type = str(random.randint(1, 1))
        super().__init__(game, pos, keys.skeleton_undertaker + '_' + type, health, strength, max_speed, agility, intelligence, stamina, 0.8, 20)
        self.Equip_Weapon(Scythe(self.game, self.pos))
        self.bones_search_cooldown = 0
        self.target_bones_collision_cooldown = 0
        self.target_bones = None
        self.active_weapon.Set_Damage(keys.vampiric, 3)
        self.intent_manager.Set_Intent([keys.direct, keys.attack, keys.attack, keys.medium_range, keys.medium_range, keys.medium_range,])

    def Update(self, tilemap, delta_time, movement=(0, 0)):
        self.Update_Bones_Search_Cooldown(delta_time)
        self.Search_For_Bones()
        self.Resurrect_Enemy()
        super().Update(tilemap, delta_time, movement)
        

    def Update_Bones_Search_Cooldown(self, delta_time):
        if not self.bones_search_cooldown:
            return
        
        self.bones_search_cooldown = max(0, self.bones_search_cooldown - delta_time)

    def Resurrect_Enemy(self):
        if not self.target_bones:
            return
        if self.target_bones_collision_cooldown:
            self.target_bones_collision_cooldown = max(0, self.target_bones_collision_cooldown - 1)
            return
        else:
            self.target_bones_collision_cooldown = 50
            self.Revive()

    def Revive(self):
        if self.target_bones and self.rect().colliderect(self.target_bones.rect()):
            self.game.particle_handler.Activate_Particles(10, keys.vampire_particle, self.rect().center)
            self.target_bones.Revive()
            self.target_bones = None
            self.bones_search_cooldown = random.randint(25, 30)
            return

    def Search_For_Bones(self):
        if self.bones_search_cooldown:
            return
        self.bones_search_cooldown = random.randint(2, 3)
        nearby_bones = self.game.tilemap.Search_Nearby_Tiles_For_Type(5, self.pos, keys.bones, self.ID)
        if not nearby_bones:
            return
            
        self.locked_on_target = False
        self.game.enemy_handler.Add_To_Pathfinding_Queue(self, nearby_bones[0].pos)
        self.Set_Movement_Strategy(keys.medium_range)
        self.target_bones = nearby_bones[0]



