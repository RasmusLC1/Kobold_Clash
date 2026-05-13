from scripts.entities.moving_entities.enemies.crypt.dwellers.dweller import Dweller
from scripts.entities.moving_entities.enemies.crypt.dwellers.vampire.vampire_intent import Vampire_Intent_Manager
from scripts.engine.keys.keys import keys


# Boss mob
class Vampire(Dweller):

    intent_manager_class = Vampire_Intent_Manager


    def __init__(self, game, pos):
        super().__init__(game, pos, keys.vampire)
        self.active_weapon.Set_Damage(keys.vampiric, 10)


