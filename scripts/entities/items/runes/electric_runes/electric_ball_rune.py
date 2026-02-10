from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.electric.electric_ball import Electric_Ball
from scripts.engine.keys.keys import keys


class Electric_Ball_Rune(Projectile_Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.electric_ball_rune, pos, 1, 25)


    def Generate_Projectile(self):
        electric_ball = Electric_Ball(self.game, self.game.player.pos, self.game.player, self.current_power, 2, 100, self.game.player.attack_direction)
        self.game.item_handler.Add_Item(electric_ball)
        self.charge = 0
        return
