import random
from scripts.engine.keys.keys import keys

class Damage_Text():
    def __init__(self):
        self.Reset()
        

    def Update(self, delta_time):
        if not self.Cooldown_Handler(delta_time):
            self.Reset()
            return False

        return True

    def Reset(self):
        self.text = None
        self.pos = None
        self.effect = None
        self.font_style = None
        self.offset = 0
        self.cooldown = 0

    def Activate(self, pos, effect, text, queue_length):
        self.effect = effect
        self.text = text
        self.pos = (pos[0] + random.randint(-10, 10), pos[1] + random.randint(-10, 10))
        self.Set_Cooldown(queue_length)
        self.Get_Font_Style(effect)

    def Get_Font_Style(self, effect):
        font_styles = {
            keys.slash : keys.font_slash,
            keys.blunt : keys.font_blunt,
            keys.fire : keys.font_fire,
            keys.frozen : keys.font_frozen,
            keys.poison : keys.font_poison,
            keys.vampiric : keys.font_vampiric,
            keys.electric : keys.font_electric,
            keys.wet : keys.font_wet,
        }
        self.font_style = font_styles.get(effect, keys.font)
        return

    def Cooldown_Handler(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time
            return True
        
        return False
    
    def Set_Cooldown(self, queue_length):
        self.offset = random.randint(15, 25)
        self.cooldown = max(0.1, random.uniform((20 - queue_length) / 30, (30 - queue_length) / 30))
