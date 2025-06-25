from scripts.entities.items.weapons.close_combat.sword import Sword
from scripts.entities.items.weapons.close_combat.halberd import Halberd
from scripts.entities.items.weapons.close_combat.torch import Torch
from scripts.entities.items.weapons.close_combat.warhammer import Warhammer
from scripts.entities.items.weapons.close_combat.battle_axe import Battle_Axe
from scripts.entities.items.weapons.close_combat.sceptre import Sceptre
from scripts.entities.items.weapons.close_combat.bell import Bell
from scripts.entities.items.weapons.close_combat.scythe import Scythe
from scripts.entities.items.weapons.close_combat.staff import Staff

from scripts.entities.items.weapons.projectiles.spear import Spear
from scripts.entities.items.weapons.projectiles.hatchet import Hatchet
from scripts.entities.items.weapons.projectiles.hammer import Hammer
from scripts.entities.items.weapons.projectiles.arrow import Arrow

from scripts.entities.items.weapons.ranged_weapons.bow import Bow
from scripts.entities.items.weapons.ranged_weapons.crossbow import Crossbow
from scripts.entities.items.weapons.shields.shield import Shield
from scripts.engine.assets.keys import keys

import random

class Weapon_Handler():
    def __init__(self, game):
        self.game = game

        # Map weapon names to their classes
        self.weapon_map = {
            keys.sword: Sword,
            keys.halberd : Halberd,
            keys.hatchet : Hatchet,
            keys.hammer : Hammer,
            keys.warhammer : Warhammer,
            keys.battle_axe : Battle_Axe,
            keys.staff : Staff,
            keys.shield : Shield,
            keys.spear : Spear,
            keys.torch : Torch,
            keys.sceptre : Sceptre,
            keys.bell : Bell,
            keys.scythe : Scythe,
            keys.bow : Bow,
            keys.crossbow : Crossbow,
        }

        self.random_weapon_map = {
            Sword: 1,
            Halberd: 1,
            Hatchet: 1,
            Hammer: 1,
            Warhammer: 0.5,
            Staff: 0.2,
            Battle_Axe: 1,
            Spear: 1,
            Sceptre: 0.3,
            Bell: 0.5,
            Scythe: 0.3,
            Bow: 1,
            Crossbow: 0.5,
            Arrow: 4,
        }



    def Weapon_Spawner(self, name, pos_x, pos_y, amount=0, data=None):
        # Handle special cases first
        if keys.particle in name:
            return True  # or your specific logic for particles

        if keys.arrow in name:
            weapon = Arrow(self.game, (pos_x, pos_y), amount)
        else:
            # Lookup the class; return False if not found
            weapon_class = self.weapon_map.get(name)
            if not weapon_class:
                return None
            weapon = weapon_class(self.game, (pos_x, pos_y))

        # Load custom data if any
        if data:
            weapon.Load_Data(data)
            if weapon.equipped:
                weapon.entity = self.game.player
                weapon.Equip()

        # Finally, add to the item handler
        self.game.item_handler.Add_Item(weapon)
        return weapon

    def Spawn_Random_Weapon(self, pos):

        selected_weapon = random.choices(
                weights=list(self.random_weapon_map.values()),
                population=list(self.random_weapon_map.keys()),
                k=1
            )[0]

        weapon = selected_weapon(self.game, pos)
        # Finally, add to the item handler
        self.game.item_handler.Add_Item(weapon)
        return weapon