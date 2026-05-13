from scripts.engine.keys.keys import keys

class Ability():
    COOLDOWN_TIME = 10
    
    def __init__(self, game, entity, name, can_attack_while_triggered = False):
        self.game = game
        self.entity = entity
        self.name = name
        self.cooldown = 0
        self.trigger_cooldown = 0
        self.can_attack_while_triggered = can_attack_while_triggered
    

    def Save_Data(self):
        self.entity.saved_data['cooldown'] = self.cooldown
        self.entity.saved_data['trigger_cooldown'] = self.trigger_cooldown


    def Load_Data(self, data):
        self.cooldown = data['cooldown']
        self.trigger_cooldown = data['trigger_cooldown']

    # Returns the cooldown time before another special attack 
    def Activate(self):
        pass


    def _Reset_Attack(self):
        self._Set_Cooldown()
    
    def _Set_Cooldown(self):
        self.cooldown = self.COOLDOWN_TIME

    def Get_Cooldown(self):
        return self.cooldown


    def Update_Cooldown(self, delta_time):
        if self.cooldown <= 0:
            self.cooldown = 0
            return True
        
        self.cooldown -= delta_time
        return False
    

    # Preents constant trigger checks
    def Check_Trigger_Cooldown(self, delta_time):
        if self.trigger_cooldown <= 0:
            self.trigger_cooldown = 1
            return True
        
        self.trigger_cooldown -= delta_time
        return False


    # Returns the cooldown for now, maybe children can do more with it
    def Update(self, delta_time) -> bool:
        pass


    # Check if the ability is triggered
    def Check_If_Trigger(self) -> bool:
        pass

    # Returns True if attacking while triggered allowed, if not if cooldown is greater than 0
    def Check_If_Attack_Allowed(self):
        return self.can_attack_while_triggered