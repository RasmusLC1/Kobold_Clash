from scripts.engine.keys import keys
from scripts.entities.moving_entities.enemies.behavior.abilities.ability_config.ability_attribute import Ability_Attribute

ACTIVE_ABILITIES = {
    keys.dash =Ability_Attribute(keys.speed, False),
    keys.jump = Ability_Attribute(keys.jump, True),
    keys.run_away = Ability_Attribute(keys.),
    keys.invulnerable = Ability_Attribute(keys.invulnerable),
    keys.rage = Ability_Attribute(),
    keys.invisibility = Ability_Attribute(),
    keys.charge = Ability_Attribute(),
    keys.rally = Ability_Attribute(),
    keys.electrify = Ability_Attribute(),
}