from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.attack_handler import Attack_Handler
from scripts.entities.moving_entities.enemies.behavior.special_attacks_handler import Special_Attack_Handler
import random


class Behavior_Manager():
    def __init__(self, game, entity, behavior, max_weapon_charge):
        self.game = game
        self.entity = entity
        self.behavior = None # The attack behavior of the enemy
        self.behavior_pattern_function = None # Calls the specific method used by the enemy AI, I.E Direct_Attack()
        self.movement_strategy = None # The movement strategy used for the attack pattern
        self.max_distance = 0 # The max distance that the enemy can detect the player
        self.movement_behavior = None
        self.engagement_cooldown = 0
        self.stored_health = self.entity.health # Used to check if entity has taken damage 
        self.Set_Behavior_Pattern(behavior)
        self.retreat_options = self.Set_Retreat_Options()
        self.attack_handler = Attack_Handler(game, entity, max_weapon_charge) 
        self.special_attack_handler = Special_Attack_Handler(game, entity)



    def Update_Behavior(self, delta_time):
        if not self.Check_Player_Distance():
            return None
        
        
        # Returns False if attack is not trigged
        self.Update_Attack(delta_time)

        return self.movement_strategy
        

    def Update_Attack(self, delta_time):
        if self.attack_handler.Update_Attack(delta_time):
            return
        
        self.Check_If_Entity_Has_Attacked()
        self.behavior_pattern_function(delta_time)
    



    # Check if player is in range, if not set to Idle
    def Check_Player_Distance(self):
        if self.entity.distance_to_player < self.max_distance:  
            return True
        
        # self.Set_Idle() # Set idle if entity is outside range
        return False
    

    def Set_Idle(self, delta_time):
        if self.behavior == keys.idle and not self.entity.target:
            return
        self.Set_Behavior_Pattern(keys.idle)

    def Check_If_Entity_Has_Attacked(self):
        if not self.attack_handler.Get_Entity_Has_Attacked():
            return False

        self.attack_handler.Set_Entity_Has_Attacked(False)
        self.Calculate_Fallback_Behavior()
        self.Set_Stored_Health()
        
        return True


    def Set_Stored_Health(self):
        self.stored_health = self.entity.health
        

    def Check_If_Entity_Has_Taken_Damage(self):
        return self.entity.damaged

    def Short_Range(self, delta_time):
        if not self.Update_Engagement_Cooldown(delta_time):
            if self.Check_If_Entity_Has_Taken_Damage():
                self.Set_Movement_Strategy(keys.medium_range)
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy(keys.medium_range)
            return False
       
        return True

    def Medium_Range(self, delta_time):
        
        if not self.Update_Engagement_Cooldown(delta_time):
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy(keys.medium_range)
            return False
        
        return True
        

    def Long_Range(self, delta_time):
        if not self.Update_Engagement_Cooldown(delta_time):
            return False
        
        self.Set_Movement_Strategy(keys.long_range)
        return self.Engagement_Controller()


    def Hit_And_Run(self, delta_time):
        if not self.Update_Engagement_Cooldown(delta_time):
            if self.Check_If_Entity_Has_Taken_Damage(): # Enemies will turn around and attack if damaged
                self.Set_Movement_Strategy(keys.direct_attack)
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy(keys.direct_attack)
            return False
        
        return True


    # Calculates the fallback behavior to be dependent on the agility
    # and intelligence of enemy
    def Calculate_Fallback_Behavior(self):
        retreat_options = self.retreat_options

        if not retreat_options:
            return
        
        num_opts = len(retreat_options)
        if num_opts == 0: return None
        if num_opts == 1: return retreat_options[0]

        # Combine stats into a single factor (0.0 to 1.0)
        combined_stat = (self.entity.intelligence + self.entity.agility) / 20.0
        
        target = combined_stat * (num_opts - 1)
        
        # Generate weights using list comprehension for performance
        # use (abs(i - target) + 1) to avoid division by zero
        weights = [1.0 / (abs(i - target) + 1.0) for i in range(num_opts)]

        retreat_distance = random.choices(retreat_options, weights=weights, k=1)[0]

        self.Set_Retreat_Cooldown(retreat_distance)
        self.Set_Movement_Strategy(retreat_distance)

        return retreat_distance
    

    def Engagement_Controller(self):
        in_range = self.Check_Attack_Distance()

        if not in_range:
            return False
        
        self.attack_handler.Set_Attack_Triggered(in_range)
        return True
    
    def Set_Retreat_Cooldown(self, retreat_distance):
        cooldown_values = {
            keys.long_range : random.randint(15, 20),
            keys.medium_range : random.randint(10, 15),
            keys.short_range : random.randint(4, 10),
        }

        self.engagement_cooldown = cooldown_values.get(retreat_distance, 1) 

        return

    def Update_Engagement_Cooldown(self, delta_time):
        if self.engagement_cooldown <= 0:
            return True
        
        self.engagement_cooldown -= delta_time
        return False
        


    def Retreat_When_Damaged(self, delta_time):
        pass
    
    # Simple direct attack logic
    def Direct_Attack(self, delta_time):
        # increment the intent when enemy attacks
        in_range = self.Check_Attack_Distance()
        
        self.attack_handler.Set_Attack_Triggered(in_range)
        return in_range


    def Idle(self, delta_time):
        pass

    # Returns true if entity if in attack range
    def Check_Attack_Distance(self):
        # Check if the player is invisible, if yes no attack
        if self.game.player.effects.Get_Effect_Strength(keys.invisibility):
            return False
        
        return self.entity.distance_to_player < self.entity.attack_distance
        

    
    def Set_Behavior_Pattern(self, behavior_pattern):
        self.behavior = behavior_pattern
        
        attack_patterns = {
            keys.long_range: self.Long_Range,
            keys.medium_range: self.Medium_Range,
            keys.short_range: self.Short_Range,
            keys.retreat_when_damaged: self.Retreat_When_Damaged,
            keys.direct_attack: self.Direct_Attack,
            keys.hit_and_run: self.Hit_And_Run,
            keys.idle: self.Idle,
        }
        self.behavior_pattern_function = attack_patterns.get(self.behavior, self.Direct_Attack)
        self.Set_Movement_Strategy(self.behavior)

    # Distance that the enemy will search for the player in
    def Set_Max_Distance(self):
        attack_patterns = {
            keys.long_range : 450,
            keys.medium_range : 400,
            keys.short_range : 350,
            keys.retreat_when_damaged : 300,
            keys.direct_attack : 300,
            keys.hit_and_run : 300,
            keys.idle : 300
        }
        self.max_distance = attack_patterns.get(self.behavior, 300)  

    # The movement strategy which is applied to an attack pattern
    # Uses a dictionary for special attacks where the attack does not align directly
    # with the movement strategy, defence = stand still or something
    def Set_Movement_Strategy(self, movement_behavior):
        if self.movement_behavior == movement_behavior:
            return
        
        movement_patterns = {
            keys.long_range : keys.long_range,
            keys.medium_range : keys.medium_range,
            keys.short_range : keys.short_range,
            keys.direct_attack : keys.direct,
            keys.retreat_when_damaged : keys.direct,
            keys.hit_and_run : keys.direct,
            keys.run_away : keys.run_away
        }

        self.movement_behavior = movement_patterns.get(movement_behavior, keys.direct)
        self.Set_Max_Distance()

    def Set_Retreat_Options(self):
        movement_patterns = {
            keys.long_range : None,
            keys.medium_range : [keys.medium_range, keys.long_range],
            keys.short_range : [keys.short_range, keys.medium_range, keys.long_range],
            keys.direct_attack : None,
            keys.retreat_when_damaged : [keys.medium_range, keys.long_range],
            keys.hit_and_run : [keys.direct_attack, keys.short_range, keys.medium_range, keys.long_range],
            keys.run_away : [keys.long_range]
        }

        return movement_patterns.get(self.behavior, None)


    def Get_Attack_Charge(self):
        return self.attack_handler.Get_Attack_Charge()
    
    def Reset_Attack(self):
        return self.attack_handler.Reset_Attack()
    
    def Get_Movement_Behavior(self):
        return self.movement_behavior