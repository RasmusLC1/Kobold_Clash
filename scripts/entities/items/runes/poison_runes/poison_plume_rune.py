from scripts.entities.items.runes.rune import Rune
from scripts.entities.items.weapons.magic_attacks.poison.poison_plume import Poison_Plume
from scripts.engine.keys.keys import keys

class Poison_Plume_Rune(Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.poison_plume_rune, pos, 2, 30)
        self.clicked = False
        self.poison_plume = Poison_Plume(self.game.player)



    def Update(self):
        super().Update()

        self.poison_plume.Update_Clouds()

        if not self.clicked:
            return
        
        if not self.poison_plume.Update(self.current_power):
            self.clicked = False

    def Trigger_Effect(self):
        self.Trigger_Rune()
        self.clicked = True

    def Render_Animation(self, surf, offset=(0, 0)):
        pass
            
