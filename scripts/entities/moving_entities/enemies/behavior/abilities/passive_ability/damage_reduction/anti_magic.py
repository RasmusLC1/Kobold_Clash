from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys


# Prevents magic damage
@register_ability(keys.anti_magic) # add ability to registry
class Anti_Magic(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)


    def Damage_Taken(self, damage, effect, direction, attacker):
        if effect[0] != keys.slash or effect[0] != keys.blunt:
            damage = 0
        
        return damage
    