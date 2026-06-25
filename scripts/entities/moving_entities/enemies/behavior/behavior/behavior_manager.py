from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.attack_handler import Attack_Handler
from scripts.entities.moving_entities.enemies.behavior.abilities.ability_handler import Ability_Handler
from .behavior_classes import *
import random
import time

# (Assume the classes above are imported here)

class Behavior_Manager():
    def __init__(self, game, entity, behavior_key, max_weapon_charge):
        self.game = game
        self.entity = entity
        
        # State variables
        self.behavior_holder = behavior_key
        self.active_behavior_key = None
        self.current_behavior = None  # Holds the instantiated child behavior class object
        
        self.movement_strategy = None 
        self.max_distance = 0 
        self.attack_distance = 0
        self.movement_behavior = None
        self.retreat_options = []
        self.engagement_cooldown = 0
        self.last_cooldown_update = time.time()
        self.stored_health = self.entity.health 
        
        # Initializing core sub-components
        self.attack_handler = Attack_Handler(game, entity, max_weapon_charge) 
        self.ability_handler = Ability_Handler(game, entity)

        # Dynamic registry mapping keys to their responsible behavior classes
        self._behavior_registry = {
            keys.idle: lambda: Idle_Behavior(self, keys.direct, 300, (1, 1), self.Calculate_Close_Ranged_Attack_Distance()),
            keys.direct_attack: lambda: Direct_Attack_Behavior(self, keys.direct, 300, (1, 1), self.Calculate_Close_Ranged_Attack_Distance()),
            keys.long_range: lambda: Long_Range_Behavior(self, keys.long_range, 450, (5, 7), self.Calculate_Ranged_Attack_Distance(250)),
            keys.medium_range: lambda: Medium_Range_Behavior(self, keys.medium_range, 400, (3, 5), self.Calculate_Ranged_Attack_Distance(200), [keys.medium_range, keys.long_range]),
            keys.short_range: lambda: Short_Range_Behavior(self, keys.short_range, 350, (2, 4), self.Calculate_Ranged_Attack_Distance(150), [keys.short_range, keys.medium_range, keys.long_range]),
            keys.hit_and_run: lambda: Hit_And_Run_Behavior(self, keys.direct, 300, (1, 1), self.Calculate_Close_Ranged_Attack_Distance(), [keys.direct_attack, keys.short_range, keys.medium_range]),
            keys.retreat: lambda: Retreat_Behavior(self, keys.run_away, 500, (2, 4), self.Calculate_Close_Ranged_Attack_Distance())
        }
        
        # Transition to initial state
        self.Set_Behavior_Pattern(behavior_key)

    def Set_Behavior_Pattern(self, behavior_key):
        # Fallback to direct attack if the key doesn't exist
        if behavior_key not in self._behavior_registry:
            behavior_key = keys.direct_attack
            
        self.active_behavior_key = behavior_key
        
        # Instantiate the specific behavior class dynamically
        self.current_behavior = self._behavior_registry[behavior_key]()
        self.current_behavior.Enter()

    def Update_Behavior(self, delta_time):
        self.entity.Set_Player_Spotted(self.Check_Player_Distance(delta_time))
        if not self.entity.player_spotted:
            return None
        
        self.entity.Set_Target()
        
        self.Update_Attack(delta_time)
        self.ability_handler.Update(delta_time)

        # Explicitly pull the active behavior key to update the strategy layer
        self.movement_strategy = self.movement_behavior
        return self.movement_strategy
        
    def Update_Attack(self, delta_time):
        if not self.ability_handler.Check_If_Attack_Allowed():
            return
        if self.attack_handler.Update_Attack(delta_time):
            return
            
        self.current_behavior.Execute()
        self.Check_If_Entity_Has_Attacked()

    def Check_Player_Distance(self, delta_time):
        return self.ability_handler.Check_Player_Distance(self.max_distance, delta_time)
        

    def Check_Attack_Distance(self):
        if self.game.player.active_ability == keys.invisibility:
            return False
        return self.entity.distance_to_player < self.attack_distance

    def Check_If_Entity_Has_Attacked(self):
        if not self.attack_handler.Get_Entity_Has_Attacked():
            return False
        self.attack_handler.Set_Entity_Has_Attacked(False)
        self.Set_Fallback_Behavior()
        self.Set_Stored_Health()
        return True

    def Set_Idle(self):
        if self.active_behavior_key == keys.idle and not self.entity.target:
            return
        self.Set_Behavior_Pattern(keys.idle)

    def Reset_Behavior(self):
        self.Set_Behavior_Pattern(self.behavior_holder)

    def Calculate_Fallback_Behavior(self):
        if not self.retreat_options: 
            return None
        
        num_opts = len(self.retreat_options)
        if num_opts == 1: 
            return self.retreat_options[0]

        combined_stat = (self.entity.intelligence + self.entity.agility) / 20.0
        target = combined_stat * (num_opts - 1)
        
        power = 3 
        weights = [1.0 / (abs(i - target) + 1.0)**power for i in range(num_opts)]
        return random.choices(self.retreat_options, weights=weights, k=1)[0]

    def Set_Fallback_Behavior(self, retreat_key=None):
        if not retreat_key:
            retreat_key = self.Calculate_Fallback_Behavior()
        if retreat_key:
            self.Set_Behavior_Pattern(retreat_key)
        return retreat_key

    def Update_Engagement_Cooldown(self):
        current_time = time.time()
        elapsed = current_time - self.last_cooldown_update
        self.last_cooldown_update = current_time

        if self.engagement_cooldown <= 0:
            self.engagement_cooldown = 0
            return True
        
        self.engagement_cooldown -= elapsed
        return False

    def Calculate_Ranged_Attack_Distance(self, distance):
        return distance + (self.entity.intelligence * 10)
    
    def Calculate_Close_Ranged_Attack_Distance(self):
        return self.entity.size[0] * max(1.5, self.entity.agility * 0.5)

    def Set_Stored_Health(self):
        self.stored_health = self.entity.health

    def Check_If_Entity_Has_Taken_Damage(self):
        return self.entity.damaged

    # --- Pass-through handler wrappers unchanged ---
    def Save_Data(self):
        self.entity.saved_data['behavior'] = self.active_behavior_key
        self.entity.saved_data['movement_strategy'] = self.movement_strategy
        self.entity.saved_data['max_distance'] = self.max_distance
        self.entity.saved_data['movement_behavior'] = self.movement_behavior
        self.entity.saved_data['stored_health'] = self.stored_health
        self.entity.saved_data['engagement_cooldown'] = self.engagement_cooldown
        self.attack_handler.Save_Data()
        self.ability_handler.Save_Data()

    def Load_Data(self, data):
        self.movement_strategy = data['movement_strategy']
        self.max_distance = data['max_distance']
        self.movement_behavior = data['movement_behavior']
        self.stored_health = data['stored_health']
        self.engagement_cooldown = data['engagement_cooldown']
        self.Set_Behavior_Pattern(data['behavior'])
        self.attack_handler.Load_Data(data)
        self.ability_handler.Load_Data(data)

    def Damage_Taken(self, damage, effect, direction, attacker):
        return self.ability_handler.Damage_Taken(damage, effect, direction, attacker)

    def Get_Attack_Charge(self):
        return self.attack_handler.Get_Attack_Charge()
    
    def Set_Ability(self, ability_name):
        return self.ability_handler.Get_Ability(ability_name)
    
    def Reset_Attack(self):
        return self.attack_handler.Reset_Attack()
    
    def Get_Movement_Behavior(self):
        return self.movement_behavior
    
    def Render_Abilities(self, surf, offset):
        self.ability_handler.Render_Abilities(surf, offset)
        
    def Trigger_Instant_Attack(self):
        return self.attack_handler.Set_Max_Weapon_Charge(self.attack_handler.max_weapon_charge / 4)
    
    def Reset_Attack_Speed(self):
        return self.attack_handler.Reset_Max_Weapon_Charge()