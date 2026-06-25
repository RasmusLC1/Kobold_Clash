import random

class Base_Behavior:
    def __init__(self, manager, profile_key, max_dist, cooldown_range, attack_distance, retreat_opts=None):
        self.manager = manager
        self.entity = manager.entity
        self.game = manager.game
        
        # Profile specific traits
        self.profile_key = profile_key
        self.max_dist = max_dist
        self.cooldown_range = cooldown_range
        self.attack_distance = attack_distance
        self.retreat_opts = retreat_opts or []

    # Called when this behavior becomes active.
    def Enter(self):
        c_min, c_max = self.cooldown_range
        self.manager.engagement_cooldown = random.randint(c_min, c_max)
        self.manager.max_distance = self.max_dist
        self.manager.attack_distance = self.attack_distance
        self.manager.retreat_options = self.retreat_opts
        self.Set_Movement_Strategy()

    # Must be implemented by child classes. Returns True/False context if needed.
    def Execute(self):
        raise NotImplementedError

    def Set_Movement_Strategy(self):
        # The profile key defines the movement behavior type
        self.manager.movement_behavior = self.profile_key

    def Engagement_Controller(self):
        if self.manager.attack_handler.Get_Attack_Triggered():
            return False
        
        in_range = self.manager.Check_Attack_Distance()
        if not in_range:
            return False
        
        self.manager.attack_handler.Set_Attack_Triggered(in_range)
        return True