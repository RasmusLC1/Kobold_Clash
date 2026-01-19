from scripts.entities.items.weapons.close_combat.sword import Sword
from scripts.entities.items.weapons.close_combat.halberd import Halberd
from scripts.entities.items.weapons.close_combat.torch import Torch
from scripts.entities.items.weapons.close_combat.sceptre import Sceptre
from scripts.entities.items.weapons.close_combat.scythe import Scythe

from scripts.entities.items.weapons.projectiles.spear import Spear
from scripts.entities.items.weapons.projectiles.hatchet import Hatchet
from scripts.entities.items.weapons.projectiles.arrow import Arrow

from scripts.entities.items.weapons.ranged_weapons.bow import Bow
from scripts.entities.items.weapons.ranged_weapons.crossbow import Crossbow
from scripts.entities.items.weapons.shields.shield import Shield

from scripts.engine.keys.keys import keys
from scripts.engine.utility.luck_calculator import Luck_Calculator

import random

class Weapon_Handler():
    def __init__(self, game):
        self.game = game

        # Map weapon names to their classes
        self.weapon_map = {
            keys.sword: Sword,
            keys.torch : Torch,
            keys.halberd : Halberd,
            keys.spear : Spear,
            keys.bow : Bow,
            keys.sceptre : Sceptre,
            keys.hatchet : Hatchet,
            keys.crossbow : Crossbow,
            keys.scythe : Scythe,

        }

        self.random_weapon_map = {
            Sword: 1,
            # Halberd: 1,
            Spear: 1,
            # Bow: 1,
            # Sceptre: 0.3,
            # Scythe: 0.3,
            # Staff: 0.2,
            # Crossbow: 0.5,
            # Arrow: 0.5,
        }



    def Weapon_Spawner(self, type, pos_x, pos_y, value = 0, data=None):
        # Handle special cases first
        if keys.particle in type:
            return True  # or your specific logic for particles

        if keys.arrow in type:
            weapon = Arrow(self.game, (pos_x, pos_y), 1)
        else:
            # Lookup the class; return False if not found
            weapon_class = self.weapon_map.get(type)
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

        random_weapon_map = self.Modify_Arrow_Spawn_Rate()

        selected_weapon = random.choices(
                weights=list(random_weapon_map.values()),
                population=list(random_weapon_map.keys()),
                k=1
            )[0]

        weapon = selected_weapon(self.game, pos)
        # Finally, add to the item handler
        self.game.item_handler.Add_Item(weapon)
        return weapon
    


    def Modify_Arrow_Spawn_Rate(self):
        weapon_rates = self.random_weapon_map.copy()

        # If no bow, stick to default rates
        if not self.game.inventory.Check_If_Bow_Equipped():
            return weapon_rates

        arrow_amount = self.game.inventory.Get_Total_Arrows()
        base_rate = 4

        if arrow_amount < 10:
            mult = 2.5  # High priority 
        elif arrow_amount < 20:
            mult = 1.0  # Standard rate
        else:
            mult = 0.2  # Very low chance when lots of arrows
            
        weapon_rates[keys.arrow] = int(base_rate * mult)

        return weapon_rates
    
    def Spawn_Arrow_For_Trap(self, pos):
        weapon = Arrow(self.game, pos, add_arrow_to_tile=False)
        self.game.item_handler.Add_Item(weapon)
        return weapon

