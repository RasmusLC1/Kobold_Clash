from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.sword import Sword
from scripts.entities.items.weapons.projectiles.spear import Spear
from scripts.entities.moving_entities.enemies.crypt.skeleton.wight_king.wight_king_intent import Wight_King_Intent_Manager
from scripts.engine.keys.keys import keys

import random

# Boss mob
class Wight_King(Skeleton):

    intent_manager_class = Wight_King_Intent_Manager


    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.wight_king, health, strength, max_speed, agility, intelligence, stamina, 40, 50, (40, 40))

        self.animation_handler.Set_Animation_Num_Max(4)
        self.animation_handler.Set_Attack_Animation_Num_Max(4)
        self.animation_handler.Set_Attack_Animation_Num_Cooldown_Max(8)
        self.Select_Weapon()
        self.intent_manager.Set_Intent([keys.keep_position, keys.direct, 'dash', keys.attack, keys.attack, keys.medium_range,])
        self.intent_manager.Set_Intent_Cooldown_Max(120)



    def Select_Weapon(self):
        weapon = None

        random_weapon = random.randint(0, 1)

        if random_weapon == 0:
            weapon = Sword(self.game, self.pos)

        elif random_weapon == 1:
            weapon = Spear(self.game, self.pos)


        if not weapon:
            return False
        
        self.Equip_Weapon(weapon)