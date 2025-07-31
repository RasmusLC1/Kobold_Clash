from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.fire.fire_ball import Fire_Ball
from scripts.engine.keys.keys import keys


class Fire_Ball_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.fire_ball_rune, pos, 5, 40)
        self.animation_time_max = 0.5
        self.animation_size_max = 15


    def Generate_Projectile(self):
        fire_ball = Fire_Ball(self.game, self.game.player.pos, self.game.player, self.current_power, 2, 100, self.game.player.attack_direction)
        self.game.item_handler.Add_Item(fire_ball)
        self.charge = 0
        return
