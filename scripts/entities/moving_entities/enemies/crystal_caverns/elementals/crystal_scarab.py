from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental


class Crystal_Scarab(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.crystal_scarab, touching_ground = True)
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.cut, 5)
        self.Set_Ability(keys.anti_magic)


