from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.engine.keys.keys import keys


class Dash_Rune(Projectile_Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.dash_rune, pos, amount, rarity_value)
        self.effect = None

    def Generate_Projectile(self):
        self.game.player.Charge(self.game.render_scroll)
