from scripts.entities.items.runes.projectile_rune import Projectile_Rune
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.engine.keys.keys import keys

class Fire_Spray_Rune(Projectile_Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.fire_spray_rune, pos, 1, 20)
        self.animation_time_max = 0.5
        self.animation_size_max = 15
        self.fire_shooter = Flame_Thrower(self.game)
        self.ready_to_shoot = False
        self.activate_cooldown_max = 2
        self.damage = 5

    def Update(self, delta_time):
        self.Check_Shooting_Ready(delta_time)

        return super().Update(delta_time)
    
    def Check_Shooting_Ready(self, delta_time):
        if not self.charge:
            return
        
        self.ready_to_shoot = self.fire_shooter.Update(delta_time)
        if not self.ready_to_shoot:
            return
        
        self.Generate_Projectile()

    def Set_Charge(self):
        self.current_power = 4
        self.charge = self.current_power
        self.ready_to_shoot = True


    def Generate_Projectile(self):
        if not self.ready_to_shoot:
            return
        self.fire_shooter.Particle_Creation(self.game.player, self.damage, cooldown=0.5)
        self.ready_to_shoot = False
        self.charge -= 1
        if self.charge <= 0:
            self.Set_Activate_Cooldown(self.activate_cooldown_max)
        return
