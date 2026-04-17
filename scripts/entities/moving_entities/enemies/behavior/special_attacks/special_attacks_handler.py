from scripts.entities.moving_entities.enemies.behavior.special_attacks.Dash import Dash
from scripts.entities.moving_entities.enemies.behavior.special_attacks.Jump_Attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.special_attacks.run_away import Run_Away
from scripts.engine.keys.keys import keys


class Special_Attack_Handler():

    ATTACK_REGISTRY = {
        keys.dash : Dash,
        keys.jump : Jump_Attack,
        keys.run_away : Run_Away,
    }

    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        self.special_attacks = {}
        self.cooldown = 0 

    # Returns the instance if it exists, or creates it if it's in the registry.
    def Get_Attack(self, attack_name):
        if attack_name in self.special_attacks:
            return self.special_attacks[attack_name]
        
        return self.Create_New_Attack(attack_name)
    
    # Create a new attack if it doesn't exist
    def Create_New_Attack(self, attack_name):
        attack_class = self.ATTACK_REGISTRY.get(attack_name)
        if not attack_class:
            return None

        new_attack = attack_class(self.game, self.entity)
        self.special_attacks[attack_name] = new_attack
        return new_attack
    

    # Allows access like handler.dash instead of handler.Get_Attack('dash)
    def __getattr__(self, name):
        attack = self.Get_Attack(name)
        if not attack:
            raise AttributeError(f"'{type(self).__name__}' has no attack attribute '{name}'")

        # Set the attribute so __getattr__ is never called for this name again
        setattr(self, name, attack) 
        return attack
        

    # Now self.dash works automatically via __getattr__
    def Handle_Dash(self):
        
        dash_effect = self.dash 
        
        if not dash_effect.dashing:
            dash_effect.Dash()

        dash_effect.Dashing_Update()

        # Check if the dash state is specifically at the 'finished' or 'impact' frame
        if dash_effect.dashing == 1:
            self.entity.Set_Charge_To_Max()