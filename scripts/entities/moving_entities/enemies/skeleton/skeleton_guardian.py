from scripts.entities.moving_entities.enemies.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.sword import Sword
from scripts.entities.items.weapons.projectiles.spear import Spear
from scripts.entities.items.weapons.close_combat.battle_axe import Battle_Axe
from scripts.entities.items.weapons.close_combat.halberd import Halberd
from scripts.entities.items.weapons.close_combat.warhammer import Warhammer

import random
from scripts.engine.assets.keys import keys

class Skeleton_Guardian(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.skeleton_guardian, health, strength, max_speed, agility, intelligence, stamina, 60)
        self.Select_Weapon()
        self.intent_manager.Set_Intent(['direct', 'attack', 'attack', 'attack', 'attack', 'attack', 'medium_range'])

    def Select_Weapon(self):
        # List of weapon classes
        weapon_classes = [
            Sword,
            Spear,
            Battle_Axe,
            Halberd,
            Warhammer,
        ]

        # Randomly select a weapon class
        selected_weapon_class = random.choice(weapon_classes)

        # Instantiate the selected weapon
        weapon = selected_weapon_class(self.game, self.pos)

        # Equip the weapon
        self.Equip_Weapon(weapon)

        self.Set_Max_Charge()



    def Set_Max_Charge(self):
        self.max_weapon_charge = self.active_weapon.speed * 15