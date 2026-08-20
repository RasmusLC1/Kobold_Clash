from .base_behavior import Base_Behavior

class Idle_Behavior(Base_Behavior):
    def Execute(self):
        pass  # Do nothing structural

class Direct_Attack_Behavior(Base_Behavior):
    def Execute(self):
        in_range = self.manager.Check_Attack_Distance()
        self.manager.attack_handler.Set_Attack_Triggered(in_range)
        return in_range # Returns a value
    

class Hit_And_Run_Behavior(Base_Behavior):
    def Execute(self):
        if not self.manager.Update_Engagement_Cooldown():
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy()
            return False
        return True # Returns a value

class Short_Range_Behavior(Base_Behavior):
    def Execute(self):
        if not self.manager.Update_Engagement_Cooldown():
            if self.manager.Check_If_Entity_Has_Taken_Damage():
                self.Set_Movement_Strategy()
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy()
            return False
        return True

class Medium_Range_Behavior(Base_Behavior):
    def Execute(self):
        if not self.manager.Update_Engagement_Cooldown():
            return False
        
        if not self.Engagement_Controller():
            self.Set_Movement_Strategy()
            return False
        return True

class Long_Range_Behavior(Base_Behavior):
    def Execute(self):
        if not self.manager.Update_Engagement_Cooldown():
            return False
        
        self.Set_Movement_Strategy()
        return self.Engagement_Controller()



class Retreat_Behavior(Base_Behavior):
    def Execute(self):
        if not self.manager.Update_Engagement_Cooldown():
            return False
        self.Set_Movement_Strategy()