from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.ice.ice_ball import Ice_Ball
from scripts.engine.keys.keys import keys

class Freeze_Ball_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.freeze_ball_rune, pos, 1, 40)
        self.animation_time_max = 0.5
        self.animation_size_max = 15



    def Generate_Projectile(self):
        ice_ball = Ice_Ball(self.game, self.game.player.pos, self.game.player, self.current_power, 2, 100, self.game.player.attack_direction)
        self.game.item_handler.Add_Item(ice_ball)
        self.charge = 0
        return

