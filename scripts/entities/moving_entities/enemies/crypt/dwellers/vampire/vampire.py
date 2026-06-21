from scripts.entities.moving_entities.enemies.crypt.dwellers.dweller import Dweller
from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.enemy_weapons.claw import Claw


# Boss mob
class Vampire(Dweller):

    def __init__(self, game, pos):
        super().__init__(game, pos, keys.vampire)
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.vampiric, 10)


