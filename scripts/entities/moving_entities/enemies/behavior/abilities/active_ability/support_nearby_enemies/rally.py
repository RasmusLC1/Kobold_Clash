from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.support_nearby_entities import Support_Nearby_Entities
from scripts.engine.keys.keys import keys

# Increases strength of nearby enemies
class Rally(Support_Nearby_Entities):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, effect_name = keys.strength, particle_name = keys.strength_particle, radius = 200)
