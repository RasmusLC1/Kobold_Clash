from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys



@register_ability(keys.echo_location) # add ability to registry
class Echo_Location(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        # Register the distance checking function strategy
        self.entity.intent_manager.behavior_manager.ability_handler.Set_Player_Distance(self.name)
        
        # Subscribe to active sound events
        self.game.enemy_handler.clatter_subscription.Subscribe_To_Acoustics(self.entity)


    def On_Clatter_Heard(self, clatter_pos):
        if not self.Check_If_Trigger():
            return

        # Add this specific entity directly to the active pathfinding queue
        self.entity.Set_Target(clatter_pos)
        self.entity.Set_Locked_On_Target(10) # Set 10 seconds lock

    def Check_If_Trigger(self) -> bool:
        if self.entity.locked_on_target:
            return False
        return True