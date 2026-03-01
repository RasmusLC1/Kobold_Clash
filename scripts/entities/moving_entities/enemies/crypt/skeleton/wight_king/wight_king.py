from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.entities.moving_entities.enemies.crypt.skeleton.wight_king.wight_king_intent import Wight_King_Intent_Manager
from scripts.engine.keys.keys import keys

import random

# Boss mob
class Wight_King(Skeleton):

    intent_manager_class = Wight_King_Intent_Manager


    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.wight_king, health, strength, max_speed, agility, intelligence, stamina, 0.6, 50, 0, 4, 4, (40, 40), attack_speed = (0.4, 0.6))
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.slash, 10)

        self.intent_manager.Set_Movement_Intent([keys.keep_position, keys.direct, 'dash',   keys.medium_range,])
        self.intent_manager.Set_Movement_Intent_Cooldown_Max(120)


