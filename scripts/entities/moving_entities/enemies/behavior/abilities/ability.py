from scripts.engine.keys.keys import keys
import time

class Ability():
    COOLDOWN_TIME = 10
    
    def __init__(self, game, entity, name, can_attack_while_triggered, is_passive):
        self.game = game
        self.entity = entity
        self.name = name
        self.cooldown = 0
        self.last_cooldown_update = time.time()
        self.trigger_cooldown = 0
        self.can_attack_while_triggered = can_attack_while_triggered
        self.is_passive = is_passive
    

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
        pass
    
    def _Set_Cooldown(self):
        pass

    def Get_Cooldown(self):
        return self.cooldown
    
    def Update_Cooldown(self):
        return True
    
    # Preents constant trigger checks
    def Check_Trigger_Cooldown(self, delta_time):
        return True
    
    def Update(self, delta_time) -> bool:
        pass

    # Check if the ability is triggered
    def Check_If_Trigger(self) -> bool:
        pass

    # Returns True if attacking while triggered allowed, if not if cooldown is greater than 0
    def Check_If_Attack_Allowed(self):
        return self.can_attack_while_triggered
    

    # Intercept, modify, and return damage calculations
    def Damage_Taken(self, damage, effect, direction, attacker):
        return damage
    
    def Render_Symbol(self, surf, offset):
        pass

    # Draw passive visual UI overlays
    def Render(self, surf, offset):
        pass