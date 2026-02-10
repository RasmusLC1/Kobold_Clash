from scripts.entities.items.runes.rune import Rune

import random
from scripts.engine.keys.keys import keys

class Passive_Rune(Rune):
    def __init__(self, game, type, pos, strength, timer_length_max, chance_to_trigger, rarity_value):
        super().__init__(game, type, pos, strength, rarity_value)
        self.count_down = 0
        self.activate_effect = False
        # Chance to trigger from 0 to 100
        self.chance_to_trigger = chance_to_trigger
        # How long between each trigger
        self.timer_length_max = timer_length_max

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['count_down'] = self.count_down
    
    def Load_Data(self, data):
        super().Load_Data(data)
        self.count_down = data['count_down'] 

    def Update(self, delta_time):
        super().Update(delta_time)

        self.Update_Count_Down(delta_time)
        self.Trigger_Effect()

    def Update_Count_Down(self, delta_time):
        if self.count_down >= self.timer_length_max:
            self.activate_effect = True
            self.count_down = 0
            return
        
        self.count_down += delta_time

    def Trigger_Effect(self): # Seperate Trigger effect from Activate
        if not self.activate_effect:
            return
        self.activate_effect = False
        trigger_value = random.randint(0, 100)
        if trigger_value < self.chance_to_trigger:
            self.game.player.Set_Effect(self.effect, self.current_power)
            self.Set_Animation_Time()
            self.Reset_Animation_Size()


    def Activate(self):
        pass