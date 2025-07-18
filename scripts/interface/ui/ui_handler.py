from scripts.interface.ui.health_bar import Health_Bar
from scripts.interface.ui.souls import Souls
from scripts.interface.ui.awakening_skull import Awakening_Skull


class UI_Handler():
    def __init__(self, game):
        self.game = game
        self.health_bar = Health_Bar(self.game)
        self.souls_interface = Souls(self.game)
        self.awakening_skull = Awakening_Skull(self.game)


    def Update(self, delta_time):
        self.health_bar.Update(delta_time)
        self.souls_interface.Update(delta_time)
        self.awakening_skull.Update(delta_time)

    def Set_Awakening_Level(self, awakening_level):
        self.awakening_skull.Set_Awakening(awakening_level)


    def Render(self, surf):
        self.souls_interface.Render(surf)
        self.health_bar.Render(surf)
        self.awakening_skull.Render(surf)