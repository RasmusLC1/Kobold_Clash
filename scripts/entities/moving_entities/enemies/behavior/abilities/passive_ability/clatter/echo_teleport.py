from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
import random
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys
import math

TELEPORT_DISTANCE = 200
TELEPORT_COOLDOWN_MAX = 10.0

@register_ability(keys.echo_teleport)
class Echo_Teleport(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.teleport_cooldown = 0.0
        self.game.enemy_handler.clatter_subscription.Subscribe_To_Acoustics(self.entity)

    def Update(self, delta_time):
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= delta_time

    def On_Clatter_Heard(self, clatter_pos):
        if self.teleport_cooldown > 0:
            return

        if not self.Check_If_Trigger():
            return

        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, TELEPORT_DISTANCE)

        target_x = clatter_pos[0] + radius * math.cos(angle)
        target_y = clatter_pos[1] + radius * math.sin(angle)

        self.entity.Set_Position((int(target_x), int(target_y)))
        self.teleport_cooldown = TELEPORT_COOLDOWN_MAX

    def Check_If_Trigger(self) -> bool:
        return self.entity.distance_to_target > TELEPORT_DISTANCE