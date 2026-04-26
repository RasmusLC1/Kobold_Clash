from scripts.entities.moving_entities.enemies.behavior.abilities.Dash import Dash
from scripts.entities.moving_entities.enemies.behavior.abilities.Jump_Attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.abilities.run_away import Run_Away
from scripts.entities.moving_entities.enemies.behavior.abilities.invincible import Invincible
from scripts.entities.moving_entities.enemies.behavior.abilities.rage import Rage

from scripts.engine.keys.keys import keys


class Ability_Handler():

    ATTACK_REGISTRY = {
        keys.dash : Dash,
        keys.jump : Jump_Attack,
        keys.run_away : Run_Away,
        keys.invincible : Invincible,
        keys.rage : Rage,
    }

    def __init__(self, game, entity, ability):
        self.game = game
        self.entity = entity
        self.abilities = {}
        self.active_attack = None
        self.cooldown = 0 

    def Update(self, delta_time):
        if not self.active_attack:
            return False
        
        if not self.active_attack.Update(delta_time):
            self.Set_Active_Attack(None)

        return True

    # Returns the instance if it exists, or creates it if it's in the registry.
    def Get_Attack(self, attack_name):
        if attack_name in self.abilities:
            return self.abilities[attack_name]
        
        return self.Create_New_Attack(attack_name)
    
    # Create a new attack if it doesn't exist
    def Create_New_Attack(self, attack_name):
        attack_class = self.ATTACK_REGISTRY.get(attack_name)
        if not attack_class:
            return None

        new_attack = attack_class(self.game, self.entity)
        self.abilities[attack_name] = new_attack
        return new_attack
    

    def Trigger_Attack(self, name):
        ability = self.abilities.get(name, None)
        if not ability:
            return False
        
        if not ability.Activate():
            return False

        self.Set_Active_Attack(ability)
        return True
    

    def Set_Active_Attack(self, attack):
        self.active_attack = attack
    
    # Allows access like handler.dash instead of handler.Get_Attack('dash)
    def __getattr__(self, name):
        attack = self.Get_Attack(name)
        if not attack:
            raise AttributeError(f"'{type(self).__name__}' has no attack attribute '{name}'")

        # Set the attribute so __getattr__ is never called for this name again
        setattr(self, name, attack) 
        return attack
        

    def Assign_Special_Attacks(self):
        enemy_types = {
            keys.earth_elemental : [keys.invincible],
            keys.ice_spirit : [keys.run_away],
            keys.minotaur : [keys.rage],
        }

        attacks_to_add = enemy_types.get(self.entity.type, [])

        for attack_key in attacks_to_add: 
            self.Create_New_Attack(attack_key)


    def Handle_Dash(self):
        
        dash_effect = self.dash 
        
        if not dash_effect.dashing:
            dash_effect.Dash()

        dash_effect.Dashing_Update()

        # Check if the dash state is specifically at the 'finished' or 'impact' frame
        if dash_effect.dashing == 1:
            self.entity.Set_Charge_To_Max()
