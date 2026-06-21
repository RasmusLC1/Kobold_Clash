from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys
import time
COOLDOWN_TIME = 50
# Increases speed when enemy spots the player
class Active_Ability(Ability):
    def __init__(self, game, entity, name, can_attack_while_triggered = False):
        super().__init__(game, entity, name, can_attack_while_triggered, is_passive = False)

    def _Reset_Attack(self):
        self._Set_Cooldown()
    
    def _Set_Cooldown(self):
        self.cooldown = self.COOLDOWN_TIME

    def Update_Cooldown(self):
        current_time = time.time()
        elapsed = current_time - self.last_cooldown_update
        self.last_cooldown_update = current_time

        if self.cooldown > 0:
            self.cooldown -= elapsed

        if self.cooldown <= 0:
            self.cooldown = 0 
            return True      
        
        return False      
    
    # Preents constant trigger checks
    def Check_Trigger_Cooldown(self, delta_time):
        if self.trigger_cooldown <= 0:
            self.trigger_cooldown = 1
            return True
        
        self.trigger_cooldown -= delta_time
        return False