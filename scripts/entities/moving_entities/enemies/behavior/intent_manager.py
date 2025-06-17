import random
from scripts.engine.assets.keys import keys

class Intent_Manager():
    def __init__(self, game, entity) -> None:
        self.game = game
        self.entity = entity

        self.current_intent = 'idle'
        self.intent = [] # Enemy's attack pattern and intent
        self.intent_index = 0
        self.intent_length = 0
        self.intent_cooldown = 0
        self.intent_cooldown_max = 200 # Lower value means faster response rate
        self.attack_cooldown = 0
        self.attack_cooldown_max = round(self.entity.max_weapon_charge * 1.2)
        self.base_cooldown = {
            "direct": 0,
            "attack": 0,
            'long_range': self.intent_cooldown_max * 2,
            "medium_range": self.intent_cooldown_max,
            "short_range": self.intent_cooldown_max,
            "keep_position": self.intent_cooldown_max * 0.5,
        }
        # Lambda stores the function to be called later
        self.actions = {
            "direct":       lambda: self.Set_Attack_Strategy("direct"),
            "long_range":   lambda: self.Set_Attack_Strategy("long_range"),
            "medium_range": lambda: self.Set_Attack_Strategy("medium_range"),
            "short_range":  lambda: self.Set_Attack_Strategy("short_range"),
            "keep_position":lambda: self.Set_Attack_Strategy("keep_position"),
            "idle" : self.Set_Idle(),
            "attack": self.Update_Attack_Cooldown,
        }
        # self.Set_Attack_Strategy(entity.attack_strategy)


    def Save_Data(self):
        self.entity.saved_data['intent_cooldown'] = self.intent_cooldown
        self.entity.saved_data['intent_index'] = self.intent_index


    def Load_Data(self, data):
        self.intent_cooldown = data['intent_cooldown']
        self.intent_index = data['intent_index']

    
    # Update the entity's behavior
    def Update_Behavior(self):
        if self.entity.distance_to_player > 300:  # skip if out of range
            if not self.current_intent == 'idle':
                self.current_intent = 'idle'
            return

        self.Handle_Attack()

        if not self.Update_Intent_Cooldown():
            return

        self.current_intent = self.intent[self.intent_index]
        action_function = self.actions.get(self.current_intent, 'idle')
        if action_function:
            action_function()
        else:
            print(f"Intent '{self.current_intent}' missing or unrecognized.")
        return

    # setting the player's attack strategy
    def Set_Attack_Strategy(self, strategy):
        self.entity.Set_Attack_Strategy(strategy)
        self.Set_Intent_Cooldown()
        self.Increment_Intent()

    def Set_Idle(self):
        self.entity.Set_Attack_Strategy('idle_find_path')
        self.Set_Intent_Cooldown()
        self.intent_index = random.randint(0, self.intent_length - 1)


    def Set_Intent(self, intent):
        self.intent = intent
        self.intent_length = len(self.intent)

    def Increment_Intent(self):
        self.intent_index += 1
        # Cycle back to the beginning if index exceeds length
        if self.intent_index >= self.intent_length:
            self.intent_index = 0

    def Set_Intent_Cooldown_Max(self, value):
        self.intent_cooldown_max = value


    def Set_Intent_Cooldown(self):
        max_cooldown = self.base_cooldown.get(self.intent[self.intent_index], self.intent_cooldown_max)
        if not max_cooldown:
            return
        try:
            self.intent_cooldown = random.randint(max_cooldown, (max_cooldown +  max_cooldown // 3))
        except Exception as e:
                print(f"WRONG INTENT COOLDOWN: {e}", max_cooldown, (max_cooldown +  max_cooldown // 3))

    # Return false on when cooldown is active
    def Update_Intent_Cooldown(self):
        if not self.intent_cooldown:
            return True
        self.intent_cooldown = max(0, self.intent_cooldown - 1)
        return False
        
    def Set_Intent_Index(self, index):
        if index >= self.intent_length:
            print("index exceed intent length", index, self.intent_length)
            return
        self.intent_index = index


    # Handle the enemy attack logic
    def Handle_Attack(self):
        # self.Update_Attack_Cooldown()
        # increment the intent when enemy attacks
        if self.entity.distance_to_player < self.entity.attack_distance:
            self.entity.Attack()
            
            return False

        if  self.entity.charge:
            self.entity.charge = 0
            self.attack_cooldown = 0

        return True

    # Updates the attack intent independent of the enemy's success with attacking to prevent it getting stuck
    def Update_Attack_Cooldown(self):
        if self.attack_cooldown >= self.attack_cooldown_max:
            self.Increment_Intent()
            self.attack_cooldown = 0
            return
        
        self.attack_cooldown += 1