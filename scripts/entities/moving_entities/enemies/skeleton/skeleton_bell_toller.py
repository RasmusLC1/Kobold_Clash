from scripts.entities.moving_entities.enemies.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.bell import Bell
from scripts.engine.keys.keys import keys

import random


class Skeleton_Bell_Toller(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        type = str(random.randint(1, 1))
        super().__init__(game, pos, keys.skeleton_bell_toller + '_' + type, health, strength, max_speed, agility, intelligence, stamina, 80, 15)
        self.Equip_Weapon(Bell(self.game, self.pos))
        self.bell_ringing_cooldown = 0
        self.intent_manager.Set_Intent([keys.direct, keys.attack, keys.attack, keys.medium_range])


    def Update(self, tilemap, movement=(0, 0)):
        self.Update_Bell_Ringing_Cooldown()
        super().Update(tilemap, movement)

    def Update_Bell_Ringing_Cooldown(self):
        if not self.bell_ringing_cooldown:
            return
        
        self.bell_ringing_cooldown = max(0, self.bell_ringing_cooldown - 1)

    def Ring_Bell(self):
        if self.bell_ringing_cooldown:
            return
        self.Generate_Sound('bell', 0.3, 1000)

        self.bell_ringing_cooldown = 3000


    def Attack(self):
        if not super().Attack():
            return False
        self.Ring_Bell()

