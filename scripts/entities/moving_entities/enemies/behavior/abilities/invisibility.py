from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys


COOLDOWN_TIME = 5
class Invisibility(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.Apply_Intelligence_Mod()



    def Apply_Intelligence_Mod(self):
        self.invisibility_level = self.entity.intelligence 
        self.light_level_limit = 100 + self.entity.intelligence * 15
        self.player_min_distance = 150 - self.entity.intelligence * 10
        self.COOLDOWN_TIME = min(0.1, 10 - self.entity.intelligence) 
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.entity.Set_Effect(keys.invisibility, self.invisibility_level, permanent=True)
        return True
    
    def Update(self, delta_time):
        if self.entity.light_level > self.light_level_limit or self.entity.distance_to_player < self.player_min_distance:
            self._Reset_Attack()
        return super().Update(delta_time)
        
    # Returns true if entity is damaged 30% of health
    def Check_If_Trigger(self):
        return self.entity.light_level <= self.light_level_limit
    
    def _Reset_Attack(self):
        self.entity.Remove_Effect(keys.invisibility, self.invisibility_level)
        return super()._Reset_Attack()