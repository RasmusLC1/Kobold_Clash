from scripts.engine.keys.keys import keys

class Special_Attack():
    COOLDOWN_TIME = 10
    
    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        self.cooldown = 0
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        self.Set_Cooldown()

    def Handle_After_Activated(self):
        pass

    
    def Set_Cooldown(self):
        self.cooldown = self.COOLDOWN_TIME


    def Update_Cooldown(self, delta_time):
        if self.cooldown <= 0:
            return True
        
        self.cooldown -= delta_time
        return False

    def Update(self, delta_time):
        if not self.Update_Cooldown(delta_time):
            return False
        
        return True