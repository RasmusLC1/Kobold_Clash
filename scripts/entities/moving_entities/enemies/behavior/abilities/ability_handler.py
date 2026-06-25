from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.dash import Dash
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.jump_attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.run_away import Run_Away
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.invulnerable import Invulnerable
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.invisibility import Invisibility
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.rage import Rage
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.charge import Charge
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.rally import Rally
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.electrify import Electrify
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.healer import Healer
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.crystal_scale import Crystal_Scale
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.gloom_stalker import Gloom_Stalker
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.bone_seeker.bone_eater import Bone_Eater
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.bone_seeker.bone_ressurector import Bone_Resurrector
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.ethereal import Ethereal
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.hearing.echo_location import Echo_Location
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.fire_born import Fire_Born
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.glacial_core import Glacial_Core
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.toxicosis import Toxicosis
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.galvanic_skin import Galvanic_Skin
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.sanguine_lord import Sanguine_Lord
from scripts.entities.moving_entities.enemies.behavior.abilities.distance_functions import Distance_Functions
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
        keys.healer : Healer,
        keys.crystal_scale : Crystal_Scale,
        keys.gloom_stalker : Gloom_Stalker,
        keys.fire_born : Fire_Born,
        keys.glacial_core : Glacial_Core,
        keys.toxicosis : Toxicosis,
        keys.galvanic_skin : Galvanic_Skin,
        keys.sanguine_lord : Sanguine_Lord,
        keys.bone_eater : Bone_Eater,
        keys.bone_ressurector : Bone_Resurrector,
        keys.ethereal : Ethereal, 
        keys.echo_location : Echo_Location, 
    }

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
    
    def Check_Player_Distance(self, max_distance):
        # Execute the active strategy function pointer, passing self context
        return self.player_distance_check_fn(self, max_distance)

    def Set_Player_Distance(self, type_key):
        # Fetch function from registry, fall back to standard if not found
        self.player_distance_check_fn = Distance_Functions.DISTANCE_REGISTRY.get(type_key,
                                            Distance_Functions.DISTANCE_REGISTRY[keys.standard])


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
