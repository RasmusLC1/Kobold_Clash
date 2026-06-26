from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.healing_from_damage_type import Healing_From_Damage_Type
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys


@register_ability(keys.glacial_core) # add ability to registry
class Glacial_Core(Healing_From_Damage_Type):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, keys.frozen)

