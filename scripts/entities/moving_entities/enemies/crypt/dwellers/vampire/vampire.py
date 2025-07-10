from scripts.entities.moving_entities.enemies.crypt.dwellers.dweller import Dweller
from scripts.entities.moving_entities.enemies.crypt.dwellers.vampire.vampire_intent import Vampire_Intent_Manager
from scripts.engine.keys.keys import keys


# Boss mob
class Vampire(Dweller):

    intent_manager_class = Vampire_Intent_Manager


    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.vampire, health, strength, max_speed, agility, intelligence, stamina, 25, 50)

        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(6)
        self.active_weapon.Set_Damage(keys.vampiric, 10)

        self.intent_manager.Set_Intent([keys.direct, 'dash', keys.attack, keys.attack, keys.attack, keys.long_range, 'shoot_soul_reaper'])

