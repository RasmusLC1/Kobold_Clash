from scripts.entities.items.weapons.close_combat.sword import Sword
from scripts.entities.items.weapons.projectiles.spear import Spear
from scripts.entities.items.weapons.close_combat.battle_axe import Battle_Axe
from scripts.entities.items.weapons.close_combat.warhammer import Warhammer
from scripts.entities.items.weapons.close_combat.halberd import Halberd
from scripts.entities.items.weapons.projectiles.hatchet import Hatchet
from scripts.entities.items.weapons.projectiles.hammer import Hammer
from scripts.engine.keys.keys import keys

from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton

import random


class Skeleton_Warrior(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        type = str(random.randint(1, 3))
        super().__init__(game, pos, keys.skeleton_warrior + '_' + type, health, strength, max_speed, agility, intelligence, stamina, 1, 10)
        self.intent_manager.Set_Intent([keys.direct, keys.attack, keys.attack, keys.attack, keys.medium_range])
        self.Select_Weapon()



    def Select_Weapon(self):
        # List of weapon classes
        weapon_classes = [
            Sword,
            Spear,
            Battle_Axe,
            Halberd,
            Warhammer,
            Hatchet,
            Hammer
        ]

        # Randomly select a weapon class
        selected_weapon_class = random.choice(weapon_classes)

        # Instantiate the selected weapon
        weapon = selected_weapon_class(self.game, self.pos)

        # Equip the weapon
        self.Equip_Weapon(weapon)

        self.Set_Max_Charge()


    def Set_Max_Charge(self):
        self.max_weapon_charge = 1.8 - self.active_weapon.speed / 10