from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.active_ability import Active_Ability
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys



@register_ability(keys.invisibility) # add ability to registry
class Invisibility(Active_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.Apply_Intelligence_Mod()

    def Apply_Intelligence_Mod(self):
        self.invisibility_level = self.entity.intelligence 
        self.light_level_limit = 100 + self.entity.intelligence * 15
        self.player_min_distance = 150 - self.entity.intelligence * 10
        self.COOLDOWN_TIME = max(0.1, 10 - self.entity.intelligence) 
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.invisibility, self.invisibility_level, permanent=True)
        return True
    
    def Update(self, delta_time):
        if self.entity.damaged: # Remove invisibility if entity is damaged
            self._Reset_Attack()
            return

        if not self.Check_Invisibility_Conditions(): # Inverse the invisibility conditions to check if it should be removed
            self._Reset_Attack()

        return
        
    # Returns true if entity is damaged 30% of health
    def Check_If_Trigger(self):
        return self.Check_Invisibility_Conditions()
    
    def Check_Invisibility_Conditions(self):
        return self.entity.light_level <= self.light_level_limit and self.entity.distance_to_target >= self.player_min_distance

    def _Reset_Attack(self):
        self.entity.Remove_Effect(keys.invisibility, self.invisibility_level)
        return super()._Reset_Attack()