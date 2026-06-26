from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
import random
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys


@register_ability(keys.echo_teleport) # add ability to registry
class Echo_Teleport(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        # Subscribe to active sound events
        self.game.enemy_handler.clatter_subscription.Subscribe_To_Acoustics(self.entity)


    def On_Clatter_Heard(self, clatter_pos):
        if not self.Check_If_Trigger():
            return
        
        pos_x = clatter_pos[0] + random.randint(-100, 100)
        pos_y = clatter_pos[1] + random.randint(-100, 100)
        
        self.entity.Set_Position((pos_x, pos_y))

    def Check_If_Trigger(self) -> bool:
        if self.entity.locked_on_target:
            return False
        return True
