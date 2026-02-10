from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Light_Rune(Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.light_rune, pos, 7, 0)

    def Update(self, delta_time):
        super().Update(delta_time)

        if self.game.player.light_source.light_level < self.current_power:
            self.game.player.Update_Light_Source(self.current_power)

    def Remove_Rune_From_Inventory(self):
        self.game.player.Update_Light_Source(4)

    def Activate(self):
        pass
    
    def Render_Animation(self, surf, offset):
        pass