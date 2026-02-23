from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.engine.keys.keys import keys

class Freeze_Spray_Rune(Projectile_Rune):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.freeze_spray_rune, pos, amount, rarity_value)
        self.ice_shooter = Ice_Shooter(self.game)
        self.activate_cooldown_max = 2
        self.damage = 12



    def Update(self, delta_time):
        self.ice_shooter.Update(delta_time)
        return super().Update(delta_time)

    def Set_Charge(self):
        self.ice_shooter.Initialise_Shooting(self.player, self.power, self.damage)

