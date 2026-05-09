from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys
import math

class Dash(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.target = None

    def Update(self, delta_time):
        if self.target:
            self.entity.max_speed = min(20, self.entity.max_speed * 10)
            if self._Check_Distance(self.target) < 10:
                self._Reset_Attack()

        return super().Update(delta_time)    

    # Returns the cooldown time before another special attack 
    def Activate(self):
        if not super().Activate():
            return False
        self.target = self.entity.target
        self.entity.Set_Behavior_Pattern(keys.direct)
        return True

    def _Check_Distance(self, target):
        distance = math.sqrt((self.entity.pos[0] - target[0]) ** 2 + (self.entity.pos[1] - target[1]) ** 2)
        return distance
            
    def _Reset_Attack(self):
        self.target = None
        self.entity.Reset_Behavior()

    # Returns true if player is between 150 and 250 after
    def Check_If_Trigger(self):
        distance_to_player = self._Check_Distance(self.game.player.pos)
        return  distance_to_player > 150 and distance_to_player < 300