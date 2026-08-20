from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental

class Electric_Elemental(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.electric_elemental)

        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.electric, 2)

