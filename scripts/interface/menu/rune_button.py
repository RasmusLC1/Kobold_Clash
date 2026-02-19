from scripts.interface.menu.button import Button
import math
from scripts.engine.keys.keys import keys

# TODO: REWORK
class Rune_Button(Button):
    def __init__(self, game, pos, size, text, effect, color = (0, 0, 0)) -> None:
        super().__init__(game, pos, size, text, 'None', False, color)
        self.effect = effect

    def Activate(self, rune):
        if self.effect == keys.souls:
            amount = -1 * math.ceil(rune.original_soul_cost / 10)
            return rune.Modify_Souls_Cost(amount)

        elif self.effect == keys.power:
            # TODO: REWORK Original values no longer kept
            amount = math.ceil(rune.original_power / 10)
            return rune.Modify_Power(amount)
        
        elif self.effect == 'purchase':
            return True

    def Update(self, rune):
        self.game.mouse.Menu_Mouse_Update()
        if self.rect().colliderect(self.game.mouse.rect_pos_menu()):
            color_0 = min(250, min(self.background_color_holder[0] * 1.3, self.background_color[0] + self.button_speed))
            color_1 = min(250, min(self.background_color_holder[1] * 1.3, self.background_color[1] + self.button_speed))
            color_2 = min(250, min(self.background_color_holder[2] * 1.3, self.background_color[2] + self.button_speed))
            self.background_color = (color_0, color_1, color_2)
            self.rect_surface.fill(self.background_color)

            if self.rect().colliderect(self.game.mouse.rect_click()):
                return self.Activate(rune)
            return False
        
        self.Reset_Color()
        return False
