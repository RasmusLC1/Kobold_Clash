from scripts.engine.keys.keys import keys

class Special_Attack():
    COOLDOWN_TIME = 10
    
    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        self.cooldown = 0
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        if self.cooldown >= 0:
            return False
        
        self._Set_Cooldown()
        return True


    def _Reset_Attack(self):
        pass
    
    def _Set_Cooldown(self):
        self.cooldown = self.COOLDOWN_TIME


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
        
        return self._Check_If_Trigger() # Returns tre if attack should be triggered
       
    
    def _Check_If_Trigger(self) -> bool:
        pass