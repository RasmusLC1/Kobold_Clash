from scripts.engine.keys.keys import keys
from scripts.interface.ui.ui_interface import UI_Interface

class Awakening_Skull(UI_Interface):
    def __init__(self, game):
        pos_x = 20
        pos_y = game.screen_height / game.render_scale - 150
        animation_max = 4
        animation_cooldown_max = 30
        super().__init__(game, pos_x, pos_y, animation_max, animation_cooldown_max)

        # Use dictionary for easy lookup
        self.awakening_symbols = {
            0: self.game.assets[keys.healthbar_1],
            1: self.game.assets[keys.healthbar_1],
            2: self.game.assets[keys.healthbar_2],
            3: self.game.assets[keys.healthbar_3],
            4: self.game.assets[keys.healthbar_4],
            5: self.game.assets[keys.healthbar_5],
        }

        self.Set_Awakening(0)

    
    def Set_Awakening(self, awakening_level):
        self.current_awakening_symbol = self.awakening_symbols.get(awakening_level)

