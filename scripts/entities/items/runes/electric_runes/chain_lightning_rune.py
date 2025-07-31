from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.electric.chain_lightning import Chain_Lightning
from scripts.engine.keys.keys import keys

class Chain_Lightning_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.chain_lightning_rune, pos, 5, 40)
        self.animation_time_max = 0.5
        self.animation_size_max = 15



    def Generate_Projectile(self):
        damage = 3
        speed = 2
        electric_ball = Chain_Lightning(self.game, self.game.player.pos, self.game.player, damage, speed, 100, 100, self.game.player.attack_direction, self.current_power)
        self.game.item_handler.Add_Item(electric_ball)
        self.charge = 0
        return
