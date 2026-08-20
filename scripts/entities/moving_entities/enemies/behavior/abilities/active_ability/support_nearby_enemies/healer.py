from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.support_nearby_entities import Support_Nearby_Entities
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys



COOLDOWN_TIME = 7
# Increases strength of nearby enemies
@register_ability(keys.healer) # add ability to registry
class Healer(Support_Nearby_Entities):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, effect_name = keys.healing, particle_name = keys.gold_particle, radius=200)
        self.effect_strength *= 3 # Increase effect strength since healing counts 1 effect strength as 1 health
