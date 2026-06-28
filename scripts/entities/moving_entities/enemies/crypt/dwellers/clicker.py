from scripts.entities.moving_entities.enemies.crypt.dwellers.dweller import Dweller
from scripts.engine.keys.keys import keys


class Clicker(Dweller):

    def __init__(self, game, pos,):
        super().__init__(game, pos, keys.clicker)
        self.active_weapon.Set_Damage(keys.cut, 5)
        self.Set_Ability(keys.echo_location)