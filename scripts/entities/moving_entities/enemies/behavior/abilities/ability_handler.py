from scripts.entities.moving_entities.enemies.behavior.abilities.dash import Dash
from scripts.entities.moving_entities.enemies.behavior.abilities.jump_attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.abilities.run_away import Run_Away
from scripts.entities.moving_entities.enemies.behavior.abilities.invulnerable import Invulnerable
from scripts.entities.moving_entities.enemies.behavior.abilities.invisibility import Invisibility
from scripts.entities.moving_entities.enemies.behavior.abilities.rage import Rage

from scripts.engine.keys.keys import keys


class Ability_Handler():

    ABILITY_REGISTRY = {
        keys.dash : Dash,
        keys.jump : Jump_Attack,
        keys.run_away : Run_Away,
        keys.invulnerable : Invulnerable,
        keys.rage : Rage,
        keys.invisibility : Invisibility,
    }

    def __init__(self, game, entity, ability):
        self.game = game
        self.entity = entity
        self.abilities = {}
        self.abilities_on_cooldown = []
        self.active_ability = None
        self.Get_Ability(ability)


    def Save_Data(self):
        self.entity.saved_data['abilities_keys'] = list(self.abilities.keys())
        self.entity.saved_data['cooldown_keys'] = [a.name for a in self.abilities_on_cooldown]
        self.entity.saved_data['active_ability_key'] = self.active_ability.name if self.active_ability else None
        
        for ability in self.abilities.values():
            ability.Save_Data()

    def Load_Data(self, data):
        saved_keys = data.get('abilities_keys', [])
        self.abilities = {}
        for key in saved_keys:
            self.Get_Ability(key) # This uses your existing logic to instantiate classes

        cooldown_keys = data.get('cooldown_keys', [])
        self.abilities_on_cooldown = [self.abilities[k] for k in cooldown_keys if k in self.abilities]

        active_key = data.get('active_ability_key')
        self.active_ability = self.abilities.get(active_key) if active_key else None

        for ability in self.abilities.values():
            ability.Load_Data(data)

    
    def Update(self, delta_time):

        no_cooldowns_active = self.Update_Abilities_Cooldown()
        
        # Update any active cooldowns
        if self.active_ability:
            self.Update_Active_Ability(delta_time)
            return True 

        # If nothing is active AND no cooldowns are running, look for something new.
        if no_cooldowns_active:
            return self._Update_Abilities(delta_time)
        
        return False


    def Update_Active_Ability(self, delta_time):
        self.active_ability.Update(delta_time)

        if self.active_ability.Get_Cooldown() > 0: 
            self.Remove_Active_Ability()
    
    # Returns true if any abilities can be triggerd
    def _Update_Abilities(self, delta_time):
        for ability in self.abilities.values():
            if not ability.Check_Trigger_Cooldown(delta_time):
                continue

            if self.entity.active_ability:
                continue

            if not ability.Check_If_Trigger():
                continue

            self.Trigger_Ability(ability)
            return True
        
        return False
    
    # Filters out any abilities that are off cooldown, returns empty array if none are on cooldown
    def Update_Abilities_Cooldown(self):
        self.abilities_on_cooldown = [
            ability for ability in self.abilities_on_cooldown 
            if not ability.Update_Cooldown()
        ]
        return not self.abilities_on_cooldown


    # Returns the instance if it exists, or creates it if it's in the registry.
    def Get_Ability(self, ability):
        if ability in self.abilities:
            return self.abilities[ability]
        
        return self.Create_New_Attack(ability)
    
    # Create a new ability if it doesn't exist
    def Create_New_Attack(self, ability_name):
        ability_class = self.ABILITY_REGISTRY.get(ability_name)
        if not ability_class:
            return None

        new_ability = ability_class(self.game, self.entity, ability_name)
        self.abilities[ability_name] = new_ability
        return new_ability
    

    def Trigger_Ability(self, ability):
        if not ability:
            return False
        
        if not ability.Activate():
            return False

        if not self.entity.Set_Active_Ability(ability.name):
            return False
        
        self.Set_Active_Attack(ability)
        return True
    

    def Set_Active_Attack(self, ability):
        self.active_ability = ability

    def Remove_Active_Ability(self):
        self.abilities_on_cooldown.append(self.active_ability)
        self.active_ability = None
        self.entity.Remove_Active_Ability()
    
    # Allows access like handler.dash instead of handler.Get_Attack('dash)
    def __getattr__(self, name):
        ability = self.Get_Ability(name)
        if not ability:
            raise AttributeError(f"'{type(self).__name__}' has no ability attribute '{name}'")

        # Set the attribute so __getattr__ is never called for this name again
        setattr(self, name, ability) 
        return ability
    
    def Check_If_Attack_Allowed(self):
        if not self.active_ability:
            return True
        
        return self.active_ability.Check_If_Attack_Allowed()


    def Handle_Dash(self):
        
        dash_effect = self.dash 
        
        if not dash_effect.dashing:
            dash_effect.Dash()

        dash_effect.Dashing_Update()

        # Check if the dash state is specifically at the 'finished' or 'impact' frame
        if dash_effect.dashing == 1:
            self.entity.Set_Charge_To_Max()


    