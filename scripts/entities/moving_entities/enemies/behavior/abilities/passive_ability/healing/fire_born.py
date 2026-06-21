from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.healing_from_damage_type import Healing_From_Damage_Type
from scripts.engine.keys.keys import keys

class Fire_Born(Healing_From_Damage_Type):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, keys.fire)

