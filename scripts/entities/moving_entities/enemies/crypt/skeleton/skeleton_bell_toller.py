from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.bell import Bell
from scripts.engine.keys.keys import keys

import random


class Skeleton_Bell_Toller(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        type = str(random.randint(1, 1))
        super().__init__(game, pos, keys.skeleton_bell_toller + '_' + type, health, strength, max_speed, agility, intelligence, stamina, 1.2, 15)
        self.Equip_Weapon(Bell(self.game, self.pos))
        self.bell_ringing_cooldown = 0
        self.intent_manager.Set_Intent([keys.direct, keys.attack, keys.attack, keys.medium_range])


    def Update(self, tilemap, delta_time, movement=(0, 0)):
        self.Update_Bell_Ringing_Cooldown(delta_time)
        super().Update(tilemap, delta_time, movement)

    def Update_Bell_Ringing_Cooldown(self, delta_time):
        if not self.bell_ringing_cooldown:
            return
        
        self.bell_ringing_cooldown = max(0, self.bell_ringing_cooldown - delta_time)

    def Ring_Bell(self):
        if self.bell_ringing_cooldown:
            return
        self.Generate_Sound(keys.bell, 0.3, 1000)

        self.bell_ringing_cooldown = 30


    def Attack(self, delta_time):
        if not super().Attack(delta_time):
            return False
        self.Ring_Bell()

