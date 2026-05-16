from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys

# Increases strength of nearby enemies
class Rally(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name, effect_name = keys.strength, particle_name = keys.strength)
