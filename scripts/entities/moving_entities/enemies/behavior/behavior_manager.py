from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.attack_handler import Attack_Handler
from scripts.entities.moving_entities.enemies.behavior.abilities.ability_handler import Ability_Handler
from scripts.entities.moving_entities.enemies.behavior.behavior_profile import Behavior_Profile
import random
import time


class Behavior_Manager():
    def __init__(self, game, entity, behavior, max_weapon_charge, ability):
        self.game = game
        self.entity = entity
        self.behavior = None # The attack behavior of the enemy

        self._config = { # Config for all the different behaviors, used for open closed principle
            keys.long_range: Behavior_Profile(self.Long_Range, 450, keys.long_range, (5, 7), self.Calculate_Ranged_Attack_Distance(250)),
            keys.medium_range: Behavior_Profile(self.Medium_Range, 400, keys.medium_range, (3, 5), self.Calculate_Ranged_Attack_Distance(200), [keys.medium_range, keys.long_range]),
            keys.short_range: Behavior_Profile(self.Short_Range, 350, keys.short_range, (2, 4), self.Calculate_Ranged_Attack_Distance(150), [keys.short_range, keys.medium_range, keys.long_range]),
            keys.direct_attack: Behavior_Profile(self.Direct_Attack, 300, keys.direct, (1, 1), self.Calculate_Close_Ranged_Attack_Distance()),
            keys.hit_and_run: Behavior_Profile(self.Hit_And_Run, 300, keys.direct, (1, 1), self.Calculate_Close_Ranged_Attack_Distance(), [keys.direct_attack, keys.short_range, keys.medium_range]),
            keys.idle: Behavior_Profile(self.Idle, 300, keys.direct, (1, 1), self.Calculate_Close_Ranged_Attack_Distance()),
            keys.retreat: Behavior_Profile(self.Retreat, 500, keys.run_away, (2, 4), self.Calculate_Close_Ranged_Attack_Distance())
        }

        self.behavior_pattern_function = None # Calls the specific method used by the enemy AI, I.E Direct_Attack()
        self.movement_strategy = None # The movement strategy used for the attack pattern
        self.max_distance = 0 # The max distance that the enemy can detect the player
        self.movement_behavior = None
        self.engagement_cooldown = 0
        self.last_cooldown_update = time.time()
        self.stored_health = self.entity.health # Used to check if entity has taken damage 
        self.Set_Behavior_Pattern(behavior)
        self.behavior_holder = self.behavior
        self.attack_handler = Attack_Handler(game, entity, max_weapon_charge) 
        self.ability_handler = Ability_Handler(game, entity, ability)
        
    
    def Save_Data(self):
        self.entity.saved_data['behavior'] = self.behavior
        self.entity.saved_data['movement_strategy'] = self.movement_strategy
        self.entity.saved_data['max_distance'] = self.max_distance
        self.entity.saved_data['movement_behavior'] = self.movement_behavior
        self.entity.saved_data['stored_health'] = self.stored_health
        self.entity.saved_data['engagement_cooldown'] = self.engagement_cooldown
        self.attack_handler.Save_Data()
        self.ability_handler.Save_Data()


    def Load_Data(self, data):
        self.behavior = data['behavior']
        self.movement_strategy = data['movement_strategy']
        self.max_distance = data['max_distance']
        self.movement_behavior = data['movement_behavior']
        self.stored_health = data['stored_health']
        self.engagement_cooldown = data['engagement_cooldown']
        self.Set_Behavior_Pattern(self.behavior) # Used to reset the behavior
        self.engagement_cooldown = data['engagement_cooldown']
        self.attack_handler.Load_Data(data)
        self.ability_handler.Load_Data(data)


    def Update_Behavior(self, delta_time):
        self.entity.Set_Player_Spotted(self.Check_Player_Distance())

        if not self.entity.player_spotted:
            return None
        
        # Returns False if attack is not trigged
        self.Update_Attack(delta_time)
        
        self.ability_handler.Update(delta_time)

        return self.movement_strategy
        

    def Update_Attack(self, delta_time):
        if not self.ability_handler.Check_If_Attack_Allowed():
            return
        if self.attack_handler.Update_Attack(delta_time):
            return
        
        self.behavior_pattern_function()
        self.Check_If_Entity_Has_Attacked()
    

    # Check if player is in range, if not set to Idle
    def Check_Player_Distance(self):
        if self.entity.distance_to_player < self.max_distance:  
            return True
        
        # self.Set_Idle() # Set idle if entity is outside range
        return False
    

    def Set_Idle(self, ):
        if self.behavior == keys.idle and not self.entity.target:
            return
        self.Set_Behavior_Pattern(keys.idle)

    def Check_If_Entity_Has_Attacked(self):
        if not self.attack_handler.Get_Entity_Has_Attacked():
            return False
        self.attack_handler.Set_Entity_Has_Attacked(False)
        self.Set_Fallback_Behavior()
        self.Set_Stored_Health()
        
        return True



    def Short_Range(self):
        if not self.Update_Engagement_Cooldown():
            if self.Check_If_Entity_Has_Taken_Damage():
                self.Set_Movement_Strategy()
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy()
            return False
       
        return True

    def Medium_Range(self):
        
        if not self.Update_Engagement_Cooldown():
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy()
            return False
        
        return True
        

    def Long_Range(self):
        if not self.Update_Engagement_Cooldown():
            return False
        
        self.Set_Movement_Strategy()
        return self.Engagement_Controller()
    
    def Retreat(self):
        if not self.Update_Engagement_Cooldown():
            return False
        
        self.Set_Movement_Strategy()

    def Set_Movement_Strategy(self):
        profile = self._config.get(self.behavior)
        self.movement_behavior = profile.movement

    def Hit_And_Run(self):
        if not self.Update_Engagement_Cooldown():
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy()
            return False

        return True

    # Calculates the fallback behavior to be dependent on the agility
    # and intelligence of enemy
    def Calculate_Fallback_Behavior(self):
        retreat_options = self.retreat_options
        if not retreat_options: return None
        
        num_opts = len(retreat_options)
        if num_opts == 1: return retreat_options[0]


        # Normalize stats (Assuming max stat is 10, so combined max is 20)
        combined_stat = (self.entity.intelligence + self.entity.agility) / 20.0
        
        # Determine the "Ideal" index for this entity
        target = combined_stat * (num_opts - 1)
        
        # Use an exponent to sharpen the probability
        # A power of 2 or 3 makes the 'target' much more dominant
        power = 3 
        weights = [1.0 / (abs(i - target) + 1.0)**power for i in range(num_opts)]

        return random.choices(retreat_options, weights=weights, k=1)[0]


    def Set_Fallback_Behavior(self, retreat_key=None):
        if not retreat_key:
            retreat_key = self.Calculate_Fallback_Behavior()
        
        # Actually swap the active behavior pattern
        if retreat_key:
            self.Set_Behavior_Pattern(retreat_key)
        return retreat_key
    
    # Returns true if enemy is within range
    def Engagement_Controller(self):

        if self.attack_handler.Get_Attack_Triggered():
            return False
        in_range = self.Check_Attack_Distance()
        if not in_range:
            return False
        
        self.attack_handler.Set_Attack_Triggered(in_range)
        return True
    
    def Trigger_Instant_Attack(self):
        value = self.attack_handler.Set_Max_Weapon_Charge(self.attack_handler.max_weapon_charge / 4)
        return value
    
    def Reset_Attack_Speed(self):
        return self.attack_handler.Reset_Max_Weapon_Charge()


    def Update_Engagement_Cooldown(self):
        current_time = time.time()
        
        elapsed = current_time - self.last_cooldown_update
        
        self.last_cooldown_update = current_time

        if self.engagement_cooldown <= 0:
            self.engagement_cooldown = 0 # Clamp to 0
            return True
        
        self.engagement_cooldown -= elapsed
        return False
    
    def Retreat(self, delta_time):
        # If the cooldown is active, we are still in "retreat mode"
        if not self.Update_Engagement_Cooldown(delta_time):
            self.Set_Movement_Strategy()
            return False # Not attacking
        
        # Once cooldown expires, pick a new attack behavior
        # This prevents the enemy from being stuck in retreat forever
        self.Set_Behavior_Pattern(keys.short_range) # Or whatever your default is
        return True
        


    def Retreat_When_Damaged(self, delta_time):
        if not self.Update_Engagement_Cooldown(delta_time):
            if self.Check_If_Entity_Has_Taken_Damage(): # Enemies will turn around and attack if damaged
                self.Set_Fallback_Behavior()
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy()
            return False
        
        return True

    
    # Simple direct attack logic
    def Direct_Attack(self):
        # increment the intent when enemy attacks
        in_range = self.Check_Attack_Distance()
        
        self.attack_handler.Set_Attack_Triggered(in_range)
        return in_range


    def Idle(self):
        pass

    def Reset_Behavior(self):
        self.Set_Behavior_Pattern(self.behavior_holder)

    # Returns true if entity if in attack range
    def Check_Attack_Distance(self):
        # Check if the player is invisible, if yes no attack
        if self.game.player.active_ability == keys.invisibility:
            return False
        return self.entity.distance_to_player < self.attack_distance
   

    def Set_Behavior_Pattern(self, behavior_pattern):
        # Fallback to direct attack if the key doesn't exist
        profile = self._config.get(behavior_pattern, self._config[keys.direct_attack])
        
        self.behavior = behavior_pattern
        self.behavior_pattern_function = profile.behavior_function
        self.max_distance = profile.max_dist
        self.movement_behavior = profile.movement
        self.retreat_options = profile.retreat_opts
        self.attack_distance = profile.attack_distance
        
        # Set a random cooldown based on the profile's range
        c_min, c_max = profile.cooldown_range
        self.engagement_cooldown = random.randint(c_min, c_max)

    def Calculate_Ranged_Attack_Distance(self, distance):
        return distance + (self.entity.intelligence * 10)
    
    def Calculate_Close_Ranged_Attack_Distance(self):
        return self.entity.size[0] * max(1.5, self.entity.agility * 0.5)

    def Set_Stored_Health(self):
        self.stored_health = self.entity.health
        

    def Check_If_Entity_Has_Taken_Damage(self):
        return self.entity.damaged
    

    def Get_Attack_Charge(self):
        return self.attack_handler.Get_Attack_Charge()
    
    def Reset_Attack(self):
        return self.attack_handler.Reset_Attack()
    
    def Get_Movement_Behavior(self):
        return self.movement_behavior