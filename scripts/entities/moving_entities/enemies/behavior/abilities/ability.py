from scripts.engine.keys.keys import keys

class Ability():
    COOLDOWN_TIME = 10
    
    def __init__(self, game, entity, name, can_attack_while_triggered = False):
        self.game = game
        self.entity = entity
        self.name = name
        self.cooldown = 0
        self.can_attack_while_triggered = can_attack_while_triggered
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        if self.cooldown > 0:
            return False
        
        self._Set_Cooldown()
        return True


    def _Reset_Attack(self):
        pass
    
    def _Set_Cooldown(self):
        self.cooldown = self.COOLDOWN_TIME

    def Get_Cooldown(self):
        return self.cooldown


    def _Update_Cooldown(self, delta_time):
        if self.cooldown <= 0:
            self.cooldown = 0
            return False
        
        self.cooldown -= delta_time
        return True

    def Update(self, delta_time) -> bool:
        if not self._Update_Cooldown(delta_time):
            self._Reset_Attack()
            return False
        
        # Returns tre if attack should be triggered
        return True

    
    # Check if the ability is triggered
    def Check_If_Trigger(self) -> bool:
        pass

    # Returns True if attacking while triggered allowed, if not if cooldown is greater than 0
    def Check_If_Attack_Allowed(self):
        return self.can_attack_while_triggered