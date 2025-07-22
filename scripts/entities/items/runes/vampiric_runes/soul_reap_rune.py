from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.vampiric.soul_reap_shooter import Soul_Reap_Shooter
from scripts.engine.keys.keys import keys

class Soul_Reap_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.soul_reap_rune, pos, 1, 20)
        self.animation_time_max = 30
        self.animation_size_max = 15
        self.activate_cooldown_max = 2
        self.soul_reap_shooter = Soul_Reap_Shooter(game)


    def Generate_Projectile(self):
        self.soul_reap_shooter.Spawn_Soul_Reap(self.game.player, self.current_power * 10)
        self.Set_Activate_Cooldown(self.activate_cooldown_max)
        self.Reset_Charge()
        return
