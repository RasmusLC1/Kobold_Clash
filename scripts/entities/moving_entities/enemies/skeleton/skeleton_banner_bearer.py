from scripts.entities.moving_entities.enemies.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.sword import Sword
from scripts.engine.assets.keys import keys

import random


class Skeleton_Banner_Bearer(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.skeleton_banner_bearer, health, strength, max_speed, agility, intelligence, stamina, 60)
        self.Equip_Weapon(Sword(self.game, self.pos))
        self.rally_cooldown = 0
        self.attack_strategy = 'medium_range'
        self.intent_manager.Set_Intent(['attack'])



    def Update(self, tilemap, movement=(0, 0)):
        self.Weapon_Cooldown()
        self.Update_Rally_Cooldown()
        self.Rally_Nearby_Enemies()
        super().Update(tilemap, movement)

    def Update_Rally_Cooldown(self):
        if not self.rally_cooldown:
            return
        
        self.rally_cooldown = max(0, self.rally_cooldown - 1)

    def Rally_Nearby_Enemies(self):
        if self.rally_cooldown:
            return
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self, 200)
        if not self.nearby_enemies:
            self.rally_cooldown = 200
            return
        self.game.particle_handler.Activate_Particles(10, keys.strength_particle, self.rect().center, frame=random.randint(20, 40))
        for enemy in self.nearby_enemies:
            enemy.effects.Set_Effect(keys.increase_strength, 4)
        self.rally_cooldown = 300



