from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys

class Shield_Rune(Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.shield_rune, pos, 10, 10)
        self.clicked = False


    def Activate(self):
        if not super().Activate():
            return    
        self.clicked = True
    
    def Update(self, delta_time):
        super().Update(delta_time)
        if not self.clicked:
            return
        if self.game.mouse.left_click:
            if not self.game.player.movement_handler.Dash(self.game.render_scroll):
                return
            self.game.player.Decrease_Souls(self.current_soul_cost)
            self.clicked = False
        
        if self.game.mouse.right_click:
            self.clicked = False

