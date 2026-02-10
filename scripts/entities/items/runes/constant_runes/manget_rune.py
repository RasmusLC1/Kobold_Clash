from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Magnet_Rune(Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.magnet_rune, pos, amount, rarity_value)


    def Update(self, delta_time):
        if not self.game.player.effects.arcane_conduit.effect:
            self.game.player.Set_Effect(self.effect, self.current_power)
        return super().Update(delta_time)        

    def Remove_Rune_From_Inventory(self):
        self.game.player.effects.Remove_Effect(self.effect)

    def Activate(self):
        pass
    
    def Render_Animation(self, surf, offset):
        pass