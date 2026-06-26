from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys


# Prevents magic damage
@register_ability(keys.anti_magic) # add ability to registry
class Anti_Magic(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)


    def Damage_Taken(self, damage, effect, direction, attacker):
        # If the attack type is NOT physical, negate it entirely
        if effect not in (keys.slash, keys.blunt):
            return 0
        return damage
    