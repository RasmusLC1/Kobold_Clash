from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.engine.keys.keys import keys

class Fire_Spray_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.fire_spray_rune, pos, 1, 20)
        self.animation_time_max = 0.5
        self.animation_size_max = 15
        self.fire_shooter = Flame_Thrower(self.game)
        self.activate_cooldown_max = 2
        self.damage = 5

    def Update(self, delta_time):
        self.fire_shooter.Update(delta_time)
        return super().Update(delta_time)

    def Set_Charge(self):
        self.fire_shooter.Initialise_Shooting(self.player, self.current_power, self.damage)

 