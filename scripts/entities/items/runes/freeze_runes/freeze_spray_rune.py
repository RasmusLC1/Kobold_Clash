from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.engine.keys.keys import keys

class Freeze_Spray_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.freeze_spray_rune, pos, 1, 20)
        self.animation_time_max = 30
        self.animation_size_max = 15
        self.ice_shooter = Ice_Shooter(self.game)
        self.activate_cooldown_max = 100

    def Set_Charge(self):
        self.charge = self.current_power * 100

    def Generate_Projectile(self):
        self.charge = self.ice_shooter.Particle_Creation(self.charge ,self.game.player, self.current_power * 10)
        if self.charge <= 0:
            self.Set_Activate_Cooldown(self.activate_cooldown_max)
        else:
            self.Set_Activate_Cooldown(0)
        return

