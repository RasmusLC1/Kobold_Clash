from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.electric.electric_shooter import Electric_Shooter
from scripts.engine.keys.keys import keys

class Electric_Spray_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.electric_spray_rune, pos, 4, 20)
        self.animation_time_max = 30
        self.animation_size_max = 15
        self.electric_shooter = Electric_Shooter(self.game)
        self.activate_cooldown_max = 2

    def Set_Charge(self):
        self.charge = self.current_power * 100

    def Generate_Projectile(self):
        self.charge = self.electric_shooter.Particle_Creation(self.game.player, self.charge, self.current_power * 7)
        if self.charge <= 0:
            self.Set_Activate_Cooldown(self.activate_cooldown_max)
        else:
            self.Set_Activate_Cooldown(0)
        return
