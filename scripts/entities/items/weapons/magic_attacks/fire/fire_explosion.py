from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_explosion import Elemental_Explosion
from scripts.engine.keys.keys import keys

class Fire_Explosion(Elemental_Explosion):
    def __init__(self, game, pos, power, entity = None):
        super().__init__(game, keys.fire_explosion, keys.fire, pos, power, 3, 7, 5, entity)
        