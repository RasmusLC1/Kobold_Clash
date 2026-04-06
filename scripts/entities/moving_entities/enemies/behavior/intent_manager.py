import random
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.path_finding import Path_Finding
from scripts.entities.moving_entities.enemies.behavior.movement_strategies import Movement_Strategies
from scripts.entities.moving_entities.enemies.behavior.behavior_manager import Behavior_Manager


class Intent_Manager():
    def __init__(self, game, entity, attack_speed, path_finding_strategy, behavior) -> None:
        self.game = game
        self.entity = entity

        self.intent = [] # Enemy's attack pattern and intent
        self.intent_index = 0
        self.current_intent = ''

        self.intent_length = 0
        self.intent_cooldown = 0
        self.intent_cooldown_max = self.Calculate_Intent_Cooldown() # Higher enemy intelligence means they respond faster
        self.attack_cooldown = 0

        # TODO: Proper attack time calculation
        self.attack_speed = attack_speed
        self.attack_cooldown_max = attack_speed

        self.actions = { # Dictionary with the diffierent intents, base is all the same but some enemies have unique patterns like dash
            keys.direct:       lambda: self.Set_Movement_Strategy(keys.direct),
            keys.long_range:   lambda: self.Set_Movement_Strategy(keys.long_range),
            keys.medium_range: lambda: self.Set_Movement_Strategy(keys.medium_range),
            keys.short_range:  lambda: self.Set_Movement_Strategy(keys.short_range),
            keys.keep_position:lambda: self.Set_Movement_Strategy(keys.keep_position),
            keys.run_away:lambda: self.Set_Movement_Strategy(keys.run_away),
        }
        # Lookup for 
        self.base_cooldown = {
            keys.direct: self.intent_cooldown_max,
            keys.attack: self.intent_cooldown_max * 0.5,
            keys.idle: 0,
            keys.long_range: self.intent_cooldown_max * 2,
            keys.medium_range: self.intent_cooldown_max,
            keys.short_range: self.intent_cooldown_max * 0.8,
            keys.keep_position: self.intent_cooldown_max,
            keys.run_away : self.intent_cooldown_max * 5,
        }
 
        self.path_finding = Path_Finding(game, entity, path_finding_strategy) # Pathfinding logic for enemy
        self.movement_strategies = Movement_Strategies(game, entity) # Pathfinding logic for enemy
        self.behavior_manager = Behavior_Manager(game, entity, behavior) 




    def Save_Data(self):
        self.entity.saved_data['intent_cooldown'] = self.intent_cooldown
        self.entity.saved_data['intent_index'] = self.intent_index
        self.entity.saved_data['path_finding_strategy'] = self.path_finding.path_finding_strategy


    def Load_Data(self, data):
        self.intent_cooldown = data['intent_cooldown']
        self.intent_index = data['intent_index']
        self.path_finding.path_finding_strategy = data['path_finding_strategy']


    # Takes the average between an enemy's agility and intelligence to set the reaction rate
    def Calculate_Intent_Cooldown(self):
        return max(0.3 ,(10 - self.entity.agility + self.entity.intelligence / 2) / 2) 
    
    # Update the entity's behavior
    def Update_Intent(self, delta_time):
        self.Update_Behavior(delta_time)
        self.path_finding.Path_Finding(delta_time)
        self.behavior_manager.Update_Behavior()



    def Update_Behavior(self, delta_time):
        
        if self.entity.distance_to_player > 300:  # skip if out of range
            self.Set_Idle()
            return

        self.Handle_Attack(delta_time)

        if not self.Update_Intent_Cooldown(delta_time):
            return

        self.Set_Current_Intent(self.intent[self.intent_index])
        action_function = self.actions.get(self.current_intent)
        if action_function:
            action_function()
        else:
            print(f"Intent '{self.current_intent}' missing or unrecognized.")
        return
    

    def Find_New_Path(self):
        if not self.path_finding.Find_Shortest_Path():
            self.entity.target = None
            return False
        
        return True

    def Set_Action(self, action):
        self.Set_Current_Intent(action)
        action_function = self.actions.get(action)
        if action_function:
            action_function()
        else:
            print(f"Intent '{self.current_intent}' missing or unrecognized.")
        return

    def Set_Current_Intent(self, intent):
        self.current_intent = intent 

    # setting the player's attack strategy
    def Set_Movement_Strategy(self, strategy):
        self.Set_Movement_Intent_Cooldown()
        self.Increment_Intent()
        self.movement_strategies.Set_Movement_Strategy(strategy)

    def Set_Idle(self):
        if self.current_intent == keys.idle and not self.entity.target:
            return
        self.Set_Current_Intent(keys.idle)
        self.intent_index = random.randint(0, self.intent_length - 1)
        self.path_finding.Find_Patrol_Path()


    def Set_Movement_Intent(self, intent):
        self.intent = intent
        self.intent_length = len(self.intent)

    def Increment_Intent(self):
        self.intent_index += 1
        # Cycle back to the beginning if index exceeds length
        if self.intent_index >= self.intent_length:
            self.intent_index = 0

    def Set_Movement_Intent_Cooldown_Max(self, value):
        self.intent_cooldown_max = value


    def Set_Movement_Intent_Cooldown(self):
        max_cooldown = self.base_cooldown.get(self.intent[self.intent_index], self.intent_cooldown_max)
        
        if not max_cooldown:
            return
        try:
            offset = round(max_cooldown / 3)
            self.intent_cooldown = random.uniform(max_cooldown - offset, max_cooldown +  offset)
        except Exception as e:
            print(f"WRONG INTENT COOLDOWN: {e}", max_cooldown, offset)

    # Return false on when cooldown is active
    def Update_Intent_Cooldown(self, delta_time):

        if not self.intent_cooldown:
            return True
        self.intent_cooldown = max(0, self.intent_cooldown - delta_time)
        return False
        
    def Set_Movement_Intent_Index(self, index):
        if index >= self.intent_length:
            print("index exceed intent length", index, self.intent_length)
            return
        self.intent_index = index


    # Handle the enemy attack logic
    def Handle_Attack(self, delta_time):
        # increment the intent when enemy attacks
        if self.entity.distance_to_player < self.entity.attack_distance:
            self.entity.Attack(delta_time)
            
            return False

        if  self.entity.charge:
            self.entity.charge = 0
            self.attack_cooldown = 0
            self.attack_cooldown_max = random.uniform(self.attack_speed[0], self.attack_speed[1])

        return True

    def Movement_Strategy(self, delta_time):
        return self.movement_strategies.Movement_Strategy(delta_time)