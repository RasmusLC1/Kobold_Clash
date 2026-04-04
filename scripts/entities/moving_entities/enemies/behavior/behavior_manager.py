from scripts.engine.keys.keys import keys


class Behavior_Manager():
    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        self.Set_Behavior_Pattern()

    def Set_Behavior_Pattern(self):
        behavior = self.Aggression_Interpreter()
        
        patterns = {
            keys.long_range: self.Long_Range,
            keys.medium_range: self.Medium_Range,
            keys.short_range: self.Short_Range,
            keys.retreat_when_damaged: self.Retreat_When_Damaged,
            keys.direct_attack: self.Direct_Attack,
            keys.hit_and_run: self.Hit_And_Run,
        }
        self.behavior_pattern = patterns.get(self.entity.behavior, self.Direct_Attack)

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