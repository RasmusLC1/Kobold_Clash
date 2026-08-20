from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys

@register_ability(keys.explode_on_impact) 
class Explode_On_Impact(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)

    def Update(self, delta_time) -> bool:
        if self.entity.distance_to_target > 60:
            return False
        
        if not self.entity.pushed_entities:
            return False
        
        # Kills entity and triggers their death condition
        self.entity.health = 0
        self.entity.Delete(generate_soul=False)
        return True