from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.sceptre import Sceptre
from scripts.engine.keys.keys import keys

import random


class Skeleton_Cleric(Skeleton):
    def __init__(self, game, pos):
        type = str(random.randint(1, 1))
        super().__init__(game, pos, keys.skeleton_cleric + '_' + type)
        self.Equip_Weapon(Sceptre(self.game, self.pos))
        self.healing_cooldown = 0



    def Update(self, tilemap, delta_time, movement=(0, 0)):
        self.Update_Healing_Cooldown(delta_time)
        self.Heal_Nearby_Enemies()
        super().Update(tilemap, delta_time, movement)

    def Update_Healing_Cooldown(self, delta_time):
        if not self.healing_cooldown:
            return
        
        self.healing_cooldown = max(0, self.healing_cooldown - delta_time)

    def Heal_Nearby_Enemies(self):
        if self.healing_cooldown:
            return
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self, 200)
        if not self.nearby_enemies:
            self.healing_cooldown = 3
            return
        self.game.particle_handler.Activate_Particles(10, keys.gold_particle, self.rect().center)
        for enemy in self.nearby_enemies:
            enemy.effects.Set_Effect(keys.healing, 15)
        self.healing_cooldown = 5

