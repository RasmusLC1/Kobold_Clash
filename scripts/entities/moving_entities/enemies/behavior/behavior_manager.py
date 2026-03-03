
class Behavior_Manager():
    def __init__(self, game, entity, behavior):
        self.game = game
        self.entity = entity
        self.Set_Behavior_Pattern(behavior)

    def Set_Behavior_Pattern(self, behavior):
        patterns = {
            "Keep_Distance": self.Keep_Distance,
            "Retreat_When_Damaged": self.Retreat_When_Damaged,
            "Aggressive": self.Aggressive,
            "Hit_And_Run": self.Hit_And_Run,
        }
        self.behavior_pattern = patterns.get(behavior, self.Aggressive)


    def Keep_Distance(self):
        pass

    def Retreat_When_Damaged(self):
        pass

    def Aggressive(self):
        pass

    def Hit_And_Run(self):
        pass