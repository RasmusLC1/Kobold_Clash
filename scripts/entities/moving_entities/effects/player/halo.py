from scripts.entities.moving_entities.effects.effect import Effect
import random
from scripts.engine.keys.keys import keys

# Don't generate sound and clatter
class Halo(Effect):
    def __init__(self, entity):
        description = '1/10 chance\nto cancel damage'
        super().__init__(entity, keys.halo, 0, 0, (120, 160), description)
        self.entity_health_holder = entity.health


    def Damage_Taken(self, damage):

        damage_saved = random.randint(1, 10 - self.effect)
        entity = self.entity
        if damage_saved == 1:
            self.entity.game.particle_handler.Activate_Particles(20, keys.gold_particle, self.entity.rect().center, frame=random.randint(20, 40))
            entity.Set_Health(self.entity_health_holder)

        self.entity_health_holder = entity.health