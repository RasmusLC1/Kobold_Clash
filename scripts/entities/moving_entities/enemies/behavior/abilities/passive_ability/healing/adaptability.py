from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.healing_from_damage_type import Healing_From_Damage_Type
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys


@register_ability(keys.adaptability) # add ability to registry
class Adaptability(Healing_From_Damage_Type):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, None)

    def Damage_Taken(self, damage, effect, direction, attacker):
        # Run the standard absorption logic first
        final_damage = super().Damage_Taken(damage, effect, direction, attacker)

        # If entity took damage and there is an effect, then it will adapt to it
        # and heal next time this effect is applied
        if final_damage > 0 and effect and effect[0]:
            self.effect_name = effect[0]

        return final_damage