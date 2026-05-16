from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.dash import Dash
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.jump_attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.run_away import Run_Away
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.invulnerable import Invulnerable
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.invisibility import Invisibility
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.rage import Rage
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.charge import Charge
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.rally import Rally
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.electrify import Electrify

from scripts.engine.keys.keys import keys


class Ability_Handler():

    ABILITY_REGISTRY = {
        keys.dash : Dash,
        keys.jump : Jump_Attack,
        keys.run_away : Run_Away,
        keys.invulnerable : Invulnerable,
        keys.rage : Rage,
        keys.invisibility : Invisibility,
        keys.charge : Charge,
        keys.rally : Rally,
        keys.electrify : Electrify,
    }

    def __init__(self, game, entity, ability):
        self.game = game
        self.entity = entity
        self.passive_abilities = {}
        self.active_abilities = {}
        self.abilities_on_cooldown = []
        self.active_ability = None
        self.Get_Ability(ability)


    def Save_Data(self):
        self.entity.saved_data['active_abilities_keys'] = list(self.active_abilities.keys())
        self.entity.saved_data['passive_abilities_keys'] = list(self.passive_abilities.keys())
        self.entity.saved_data['cooldown_keys'] = [a.name for a in self.abilities_on_cooldown]
        self.entity.saved_data['active_ability_key'] = self.active_ability.name if self.active_ability else None
        
        for ability in self.active_abilities.values():
            ability.Save_Data()

        for ability in self.passive_abilities.values():
            ability.Save_Data()
            

    def Load_Data(self, data):
        self._Load_Active_Abilities(data)
        self._Load_Passive_Abilities(data)
        cooldown_keys = data.get('cooldown_keys', [])
        self.abilities_on_cooldown = [self.active_abilities[k] for k in cooldown_keys if k in self.active_abilities]

        active_key = data.get('active_ability_key')
        self.active_ability = self.active_abilities.get(active_key) if active_key else None

        for ability in self.active_abilities.values():
            ability.Load_Data(data)

    def _Load_Active_Abilities(self, data):
        saved_active_keys = data.get('active_abilities_keys', [])
        self.active_abilities = {}
        for key in saved_active_keys:
            self.Get_Ability(key)

    def _Load_Passive_Abilities(self, data):
        saved_active_keys = data.get('passive_abilities_keys', [])
        self.passive_abilities = {}
        for key in saved_active_keys:
            self.Get_Ability(key)

    
    def Update(self, delta_time):
        self._Update_Passive_Abilities(delta_time) # Passive abilities are always updated

        no_cooldowns_active = self.Update_Abilities_Cooldown()
        
        # Update any active cooldowns
        if self.active_ability:
            self._Update_Active_Ability(delta_time)
            return True 

        # If nothing is active AND no cooldowns are running, look for something new.
        if no_cooldowns_active:
            return self._Update_Active_Abilities(delta_time)
        
        return False


    def _Update_Active_Ability(self, delta_time):
        self.active_ability.Update(delta_time)

        if self.active_ability.Get_Cooldown() > 0: 
            self.Remove_Active_Ability()

    def _Update_Passive_Abilities(self, delta_time):
        if not self.passive_abilities:
            return
        
        for ability in self.passive_abilities.values():
            ability.Update(delta_time)

    
    # Returns true if any abilities can be triggerd
    def _Update_Active_Abilities(self, delta_time):
        for ability in self.active_abilities.values():
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
        if ability in self.active_abilities: # Check active abilities
            return self.active_abilities[ability]
        
        if ability in self.passive_abilities: # Check passive abilities
            return self.passive_abilities[ability]
        
        return self.Create_New_Ability(ability)
    
    # Create a new ability if it doesn't exist
    def Create_New_Ability(self, ability_name):
        ability_class = self.ABILITY_REGISTRY.get(ability_name)
        if not ability_class:
            return None

        new_ability = ability_class(self.game, self.entity, ability_name)
        self.Assign_Ability(new_ability, ability_name)
        return new_ability
    
    # Assign the ability to either passive or active dictionary
    def Assign_Ability(self, ability, ability_name):
        if ability.is_passive:
            self.passive_abilities[ability_name] = ability
        else:
            self.active_abilities[ability_name] = ability

    

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


    def Render_Abilities(self, surf, offset):
        for ability in self.passive_abilities.values():
            self._Render_Ability(ability, surf, offset)

        for ability in self.active_abilities.values():
            self._Render_Ability(ability, surf, offset)

    def _Render_Ability(self, ability, surf, offset):
        ability.Render_Symbol(surf, offset)
        ability.Render(surf, offset)

