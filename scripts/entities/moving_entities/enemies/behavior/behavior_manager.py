from scripts.engine.keys.keys import keys
import random

class Behavior_Manager():
    def __init__(self, game, entity, behavior):
        self.game = game
        self.entity = entity
        self.behavior = behavior
        self.behavior_pattern_function = None # Calls the specific method used by the enemy AI, I.E Direct_Attack()
        self.movement_strategy = None # 
        self.max_distance = 0
        self.Set_Behavior_Pattern()


    def Update_Behavior(self):
        
        self.behavior_pattern_function()

        return self.movement_strategy


    # Check if player is in range, if not set to Idle
    def Check_Player_Distance(self):
        if self.entity.distance_to_player < self.max_distance:  
            return True
        
        self.Set_Idle()
        return False

    def Set_Behavior_Pattern(self):
        
        attack_patterns = {
            keys.long_range: self.Long_Range,
            keys.medium_range: self.Medium_Range,
            keys.short_range: self.Short_Range,
            keys.retreat_when_damaged: self.Retreat_When_Damaged,
            keys.direct_attack: self.Direct_Attack,
            keys.hit_and_run: self.Hit_And_Run,
        }
        self.behavior_pattern_function = attack_patterns.get(self.behavior, self.Direct_Attack)
        self.Set_Max_Distance()


    def Set_Max_Distance(self):
        attack_patterns = {
            keys.long_range: 500,
            keys.medium_range: 400,
            keys.short_range: 350,
            keys.retreat_when_damaged: 300,
            keys.direct_attack: 300,
            keys.hit_and_run: 300,
        }
        self.max_distance = attack_patterns.get(self.behavior, 300)        


    def Set_Idle(self):
        if self.current_intent == keys.idle and not self.entity.target:
            return
        self.Set_Current_Intent(keys.idle)
        self.intent_index = random.randint(0, self.intent_length - 1)
        self.path_finding.Find_Patrol_Path()


    def Short_Range(self):
        pass

    def Medium_Range(self):
        pass

    def Long_Range(self):
        pass

    def Retreat_When_Damaged(self):
        pass

    def Direct_Attack(self):
        pass

    def Hit_And_Run(self):
        pass