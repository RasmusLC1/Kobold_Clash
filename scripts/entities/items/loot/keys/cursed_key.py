from scripts.entities.items.loot.keys.key import Key
from  scripts.entities.items.loot.curse.effect_curse import Effect_Curse
import random
from scripts.engine.keys.keys import keys

class Cursed_Key(Key):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.cursed_key, pos, rarity_value)
        self.min_curse =  max(1, 4 - amount) 
        self.max_curse =  max(1, 6 - amount)

    def Set_Description(self):
        self.description = 'Open any\ndoor and\nbe cursed'


    # Cost souls to open door
    def Open_Door(self):
        curse = Effect_Curse.Set_Random_Negative_Effect()
        intensity = random.randint(self.min_curse, self.max_curse)
        self.game.player.Set_Effect(curse, intensity)
        return True