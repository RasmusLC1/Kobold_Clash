from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.attack_handler import Attack_Handler

class Behavior_Manager():
    def __init__(self, game, entity, behavior, max_weapon_charge):
        self.game = game
        self.entity = entity
        self.behavior = None # The attack behavior of the enemy
        self.behavior_pattern_function = None # Calls the specific method used by the enemy AI, I.E Direct_Attack()
        self.movement_strategy = None # The movement strategy used for the attack pattern
        self.max_distance = 0 # The max distance that the enemy can detect the player
        self.Set_Behavior_Pattern(behavior)
        self.attack_handler = Attack_Handler(game, entity, max_weapon_charge) 



    def Update_Behavior(self, delta_time):
        if not self.Check_Player_Distance():
            return None
        
        # Returns False if attack is not trigged
        if not self.attack_handler.Update_Attack(delta_time):
            self.behavior_pattern_function()
            return self.movement_strategy
        

        return self.movement_strategy


    # Check if player is in range, if not set to Idle
    def Check_Player_Distance(self):
        if self.entity.distance_to_player < self.max_distance:  
            return True
        
        # self.Set_Idle() # Set idle if entity is outside range
        return False
    

    def Set_Idle(self):
        if self.behavior == keys.idle and not self.entity.target:
            return
        self.Set_Behavior_Pattern(keys.idle)



    def Short_Range(self):
        pass

    def Medium_Range(self):
        pass

    def Long_Range(self):
        pass

    def Retreat_When_Damaged(self):
        pass

    def Direct_Attack(self):
        # increment the intent when enemy attacks
        in_range = self.Check_Attack_Distance()
        
        self.attack_handler.Set_Attack_Triggered(in_range)
        return in_range

    def Hit_And_Run(self):
        pass

    def Idle(self):
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
        self.Set_Max_Distance()
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
        attack_patterns = {
            keys.long_range : keys.long_range,
            keys.medium_range : keys.medium_range,
            keys.short_range : keys.short_range,
            keys.direct_attack : keys.direct,
            keys.retreat_when_damaged : keys.direct,
            keys.hit_and_run : keys.direct,
            keys.run_away : keys.run_away
        }
        self.movement_strategy = attack_patterns.get(movement_behavior, keys.direct)


    def Get_Attack_Charge(self):
        return self.attack_handler.Get_Attack_Charge()
    
    def Reset_Attack(self):
        return self.attack_handler.Reset_Attack()