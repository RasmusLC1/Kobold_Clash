from scripts.entities.items.loot.keys.key import Key
from  scripts.entities.items.loot.curse.effect_curse import Effect_Curse
import random
from scripts.engine.keys.keys import keys

class Cursed_Key(Key):
    def __init__(self, game, pos):
        super().__init__(game, keys.cursed_key, pos)
        self.description = 'Open any\ndoor and\nbe cursed'
        self.curse_generator = Effect_Curse()

    # Cost souls to open door
    def Open_Door(self):
        curse = self.curse_generator.Set_Random_Negative_Effect()
        intensity = random.randint(3, 5)
        self.game.player.Set_Effect(curse, intensity)
        return True