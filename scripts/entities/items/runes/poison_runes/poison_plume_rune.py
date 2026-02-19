from scripts.entities.items.runes.rune import Rune
from scripts.entities.items.weapons.magic_attacks.poison.poison_plume import Poison_Plume
from scripts.engine.keys.keys import keys

class Poison_Plume_Rune(Rune):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.poison_plume_rune, pos, amount, rarity_value)
        self.poison_plume = Poison_Plume(self.game.player)



    def Update(self, delta_time):
        super().Update(delta_time)

        self.poison_plume.Update_Clouds()

        if not self.clicked:
            return
        
        if not self.poison_plume.Update(self.power):
            self.clicked = False

    def Trigger_Effect(self):
        self.Trigger_Rune()
        self.clicked = True

    def Render_Animation(self, surf, offset=(0, 0)):
        pass
            
