from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.poison.poison_ball import Poison_Ball
from scripts.engine.keys.keys import keys


class Poison_Ball_Rune(Projectile_Rune):
    def __init__(self, game, type, pos, rarity_value, amount):
        super().__init__(game, keys.poison_ball_rune, pos, 1, 20)


    def Generate_Projectile(self):
        poison_ball = Poison_Ball(self.game, self.game.player.pos, self.game.player, self.current_power, 2, 100, self.game.player.attack_direction)
        self.game.item_handler.Add_Item(poison_ball)
        self.charge = 0
        return

