from scripts.entities.moving_entities.enemies.behavior.abilities import registry as registry
from scripts.entities.moving_entities.enemies.behavior.abilities.distance_functions import DISTANCE_REGISTRY
from scripts.engine.keys.keys import keys

class Ability_Handler():
    @property
    def ABILITY_REGISTRY(self):
        """Always points to the live dictionary variable inside the registry module."""
        return registry.ABILITY_REGISTRY

    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        self.passive_abilities = {}
        self.active_ability = None  # Holds the single assigned active ability (or None)
        self.abilities_on_cooldown = []
        self.is_running_ability = False  # Track execution state separately from assignment
        self.Set_Player_Distance(keys.standard)

    def Save_Data(self):
        self.entity.saved_data['active_ability_key'] = self.active_ability.name if self.active_ability else None
        self.entity.saved_data['passive_abilities_keys'] = list(self.passive_abilities.keys())
        self.entity.saved_data['cooldown_keys'] = [a.name for a in self.abilities_on_cooldown]
        self.entity.saved_data['is_running_ability'] = self.is_running_ability
        
        if self.active_ability:
            self.active_ability.Save_Data()

        for ability in self.passive_abilities.values():
            ability.Save_Data()

    def Load_Data(self, data):
        self._Load_Active_Ability(data)
        self._Load_Passive_Abilities(data)
        
        cooldown_keys = data.get('cooldown_keys', [])
        self.abilities_on_cooldown = []
        if self.active_ability and self.active_ability.name in cooldown_keys:
            self.abilities_on_cooldown.append(self.active_ability)
        
        self.is_running_ability = data.get('is_running_ability', False)

    def _Load_Active_Ability(self, data):
        active_key = data.get('active_ability_key')
        self.active_ability = None
        if active_key:
            self.Get_Ability(active_key)
            if self.active_ability:
                self.active_ability.Load_Data(data)

    def _Load_Passive_Abilities(self, data):
        saved_passive_keys = data.get('passive_abilities_keys', [])
        self.passive_abilities = {}
        for key in saved_passive_keys:
            self.Get_Ability(key)

        for ability in self.passive_abilities.values():
            ability.Load_Data(data)

    def Update(self, delta_time):
        # Passives process completely independently
        for ability in self.passive_abilities.values():
            ability.Update(delta_time)

        # Handle active execution state machine
        if self.is_running_ability and self.active_ability:
            self._Update_Running_Ability(delta_time)
            return True 

        no_cooldowns_active = self.Update_Abilities_Cooldown()
        if no_cooldowns_active and self.active_ability:
            return self._Update_Active_Ability(delta_time)
        
        return False

    def _Update_Running_Ability(self, delta_time):
        self.active_ability.Update(delta_time)
        if self.active_ability.Get_Cooldown() > 0: 
            self.Remove_Active_Ability()

    def _Update_Active_Ability(self, delta_time):
        ability = self.active_ability
        
        if not ability.Check_Trigger_Cooldown(delta_time):
            return False

        if self.entity.active_ability:
            return False

        if not ability.Check_If_Trigger():
            return False

        self.Trigger_Ability(ability)
        return True

    def Update_Abilities_Cooldown(self):
        self.abilities_on_cooldown = [
            ability for ability in self.abilities_on_cooldown 
            if not ability.Update_Cooldown()
        ]
        return not self.abilities_on_cooldown

    def Get_Ability(self, ability_name):
        if self.active_ability and self.active_ability.name == ability_name:
            return self.active_ability
        
        if ability_name in self.passive_abilities:
            return self.passive_abilities[ability_name]
        
        return self.Create_New_Ability(ability_name)
    
    def Create_New_Ability(self, ability_name):
        ability_class = self.ABILITY_REGISTRY.get(ability_name)
        if not ability_class:
            return None

        new_ability = ability_class(self.game, self.entity, ability_name)
        self.Assign_Ability(new_ability, ability_name)
        return new_ability
    
    def Assign_Ability(self, ability, ability_name):
        if ability.is_passive:
            self.passive_abilities[ability_name] = ability
        else:
            self.active_ability = ability

    def Trigger_Ability(self, ability):
        if not ability or not ability.Activate():
            return False

        if not self.entity.Set_Active_Ability(ability.name):
            return False
        
        self.Set_Active_Attack()
        return True

    def Set_Active_Attack(self):
        self.is_running_ability = True

    def Remove_Active_Ability(self):
        if self.active_ability and self.active_ability not in self.abilities_on_cooldown:
            self.abilities_on_cooldown.append(self.active_ability)
        self.is_running_ability = False
        self.entity.Remove_Active_Ability()
    
    def __getattr__(self, name):
        if name in self.ABILITY_REGISTRY:
            ability = self.Get_Ability(name)
            setattr(self, name, ability) 
            return ability
        raise AttributeError(f"'{type(self).__name__}' has no registry or attribute mapping for '{name}'")
    
    def Check_If_Attack_Allowed(self):
        if not self.is_running_ability or not self.active_ability:
            return True
        return self.active_ability.Check_If_Attack_Allowed()
    
    def On_Clatter_Heard(self, clatter_pos):
        for ability in self.passive_abilities.values():
            ability.On_Clatter_Heard(clatter_pos)

    
    def Check_Player_Distance(self, max_distance, delta_time):
        # Call the .check method on our active strategy object instance
        return self.player_distance_strategy.check(max_distance, delta_time)

    def Set_Player_Distance(self, type_key):
        # Fetch the class structure layout from your registry map
        strategy_class = DISTANCE_REGISTRY.get(type_key, DISTANCE_REGISTRY[keys.standard])
        
        # Instantiate it dynamically, binding this handler context onto it
        self.player_distance_strategy = strategy_class(self)


    def Damage_Taken(self, damage, effect, direction, attacker):
        for ability in self.passive_abilities.values():
            damage = ability.Damage_Taken(damage, effect, direction, attacker)

        if self.is_running_ability and self.active_ability:
            damage = self.active_ability.Damage_Taken(damage, effect, direction, attacker)
        
        return damage

    def Render_Abilities(self, surf, offset):
        for ability in self.passive_abilities.values():
            ability.Render(surf, offset)

        self._Render_Running_Ability(surf, offset)

    def _Render_Running_Ability(self, surf, offset):
        if not self.is_running_ability:
            return 
            
        self.active_ability.Render(surf, offset)
        
        entity_pos = self.entity.pos
        render_position = (entity_pos[0] - offset[0], entity_pos[1] - offset[1])
        self.game.mixed_symbols.Render_Mixed_Text(surf, self.active_ability.name, render_position)
