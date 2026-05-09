from scripts.entities.moving_entities.enemies.behavior.abilities.dash import Dash
from scripts.entities.moving_entities.enemies.behavior.abilities.jump_attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.abilities.run_away import Run_Away
from scripts.entities.moving_entities.enemies.behavior.abilities.invulnerable import Invulnerable
from scripts.entities.moving_entities.enemies.behavior.abilities.rage import Rage

from scripts.engine.keys.keys import keys


class Ability_Handler():

    ABILITY_REGISTRY = {
        keys.dash : Dash,
        keys.jump : Jump_Attack,
        keys.run_away : Run_Away,
        keys.invulnerable : Invulnerable,
        keys.rage : Rage,
    }

    def __init__(self, game, entity, ability):
        self.game = game
        self.entity = entity
        self.abilities = {}
        self.active_ability = None
        self.cooldown = 0 
        self.Get_Ability(ability)

    
    def Update(self, delta_time):
        # Always update the active ability if it exists
        if not self.active_ability:
            # Only look for new abilities if none are active
            return self._Update_Abilities(delta_time)
        
        self.active_ability.Update(delta_time)
        
        # If the ability has finished or cooled down, clear it
        # Note: You might want a specific 'is_finished' flag instead of just cooldown
        if self.active_ability.Get_Cooldown() <= 0: 
            self.Remove_Active_Ability()
        return True

    
    # Returns true if any abilities can be triggerd
    def _Update_Abilities(self, delta_time):
        for ability in self.abilities.values():
            if not ability.Update(delta_time):
                continue

            if not ability.Check_Trigger_Cooldown(delta_time):
                continue

            if self.entity.active_ability:
                continue

            if not ability.Check_If_Trigger():
                continue

            self.Trigger_Attack(ability.name)
            return True
        
        return False

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
    

    def Trigger_Attack(self, name):
        ability = self.abilities.get(name, None)
        if not ability:
            return False
        
        if not ability.Activate():
            return False

        if not self.entity.Set_Active_Ability(name):
            return False
        
        self.Set_Active_Attack(ability)
        return True
    

    def Set_Active_Attack(self, ability):
        self.active_ability = ability

    def Remove_Active_Ability(self):
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


    