from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.engine.keys.keys import keys

class Fire_Spirit(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.fire_spirit)
        self.Set_Ability(keys.fire_born)
        self.look_for_health_cooldown = 0
        self.fire_damage = 1

        self.active_weapon = Flame_Thrower(self.game, self)

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        super().Update(tilemap, delta_time, movement)
        self.active_weapon.Update(delta_time)


