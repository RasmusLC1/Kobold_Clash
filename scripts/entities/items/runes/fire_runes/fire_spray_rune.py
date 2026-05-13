from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.engine.keys.keys import keys

class Fire_Spray_Rune(Projectile_Rune):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, type, pos, amount, rarity_value)
        self.fire_shooter = Flame_Thrower(self.game, self.game.player)
        self.activate_cooldown_max = 2
        self.damage = 5

    def Update(self, delta_time):
        self.fire_shooter.Update(delta_time)
        return super().Update(delta_time)

    def Set_Charge(self):
        self.fire_shooter.Initialise_Shooting(self.player, self.power, self.damage)

 