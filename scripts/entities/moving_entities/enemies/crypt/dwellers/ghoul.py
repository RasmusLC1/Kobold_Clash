from scripts.entities.moving_entities.enemies.crypt.dwellers.dweller import Dweller
from scripts.engine.keys.keys import keys


class Ghoul(Dweller):

    def __init__(self, game, pos,):
        super().__init__(game, pos, keys.ghoul)
        self.attack_symbol_offset = 10
        self.active_weapon.Set_Damage(keys.poison, 2)
        self.active_weapon.Set_Damage(keys.blunt, 3)
        self.Set_Ability(keys.bone_eater)

