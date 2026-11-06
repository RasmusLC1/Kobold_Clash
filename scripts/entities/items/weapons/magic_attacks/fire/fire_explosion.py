from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_explosion import Elemental_Explosion
from scripts.engine.keys.keys import keys

class Fire_Explosion(Elemental_Explosion):
    def __init__(self, game, pos, power, entity = None):
        super().__init__(game, keys.fire_explosion, keys.fire, pos, power,
                         effect_strength=3, max_animation=7,
                         animation_cooldown_max=0.1, entity=entity)
        