from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental


class Earth_Elemental(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.earth_elemental, 3, 3, 3, size=(48, 48), attack_speed=(0.7, 1))
        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.blunt, 5)


