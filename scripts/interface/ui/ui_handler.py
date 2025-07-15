from scripts.interface.ui.health_bar import Health_Bar
from scripts.interface.ui.souls import Souls
from scripts.interface.ui.awakening_skull import Awakening_Skull


class UI_Handler():
    def __init__(self, game):
        self.game = game
        self.health_bar = Health_Bar(self.game)
        self.souls_interface = Souls(self.game)
        self.awakening_skull = Awakening_Skull(self.game)


    def Update(self):
        self.health_bar.Update()
        self.souls_interface.Update()
        self.awakening_skull.Update()


    def Render(self, surf):
        self.souls_interface.Render(surf)
        self.health_bar.Render(surf)
        self.awakening_skull.Render(surf)