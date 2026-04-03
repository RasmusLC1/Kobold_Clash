from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys

import random


class Skeleton_Banner_Bearer(Skeleton):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.skeleton_banner_bearer, default_range=keys.medium_range)
        self.Equip_Weapon(Claw(self.game, self.pos))
        self.active_weapon.Set_Damage(keys.slash, 5)
        self.rally_cooldown = 0
        self.intent_manager.Set_Movement_Intent([keys.medium_range])



    def Update(self, tilemap, delta_time, movement=(0, 0)):
        self.Update_Rally_Cooldown(delta_time)
        self.Rally_Nearby_Enemies()
        super().Update(tilemap, delta_time, movement)

    def Update_Rally_Cooldown(self, delta_time):
        if not self.rally_cooldown:
            return
        
        self.rally_cooldown = max(0, self.rally_cooldown - delta_time)

    def Rally_Nearby_Enemies(self):
        if self.rally_cooldown:
            return
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self, 200)
        if not self.nearby_enemies:
            self.rally_cooldown = 3
            return
        self.game.particle_handler.Activate_Particles(10, keys.strength_particle, self.rect().center)
        for enemy in self.nearby_enemies:
            enemy.effects.Set_Effect(keys.increase_strength, 4)
        self.rally_cooldown = 5



