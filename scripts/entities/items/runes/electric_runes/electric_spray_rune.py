from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.electric.electric_shooter import Electric_Shooter
from scripts.engine.keys.keys import keys

class Electric_Spray_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.electric_spray_rune, pos, 4, 20)
        self.electric_shooter = Electric_Shooter(self.game)
        self.activate_cooldown_max = 2
        self.damage = 10


    def Update(self, delta_time):
        self.electric_shooter.Update(delta_time)
        return super().Update(delta_time)

    def Set_Charge(self):
        self.electric_shooter.Initialise_Shooting(self.player, self.current_power, self.damage)


