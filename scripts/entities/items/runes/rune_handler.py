from scripts.entities.items.runes.basic_runes.healing_rune import Healing_Rune
from scripts.entities.items.runes.basic_runes.invisibility_rune import Invisibility_Rune
from scripts.entities.items.runes.basic_runes.strength_rune import Strength_Rune
from scripts.entities.items.runes.basic_runes.silence_rune import Silence_Rune
from scripts.entities.items.runes.basic_runes.speed_rune import Speed_Rune
from scripts.entities.items.runes.basic_runes.vampiric_rune import Vampiric_Rune
from scripts.entities.items.runes.basic_runes.invulnerable_rune import Invulnerable_Rune

from scripts.entities.items.runes.random_runes.dash_rune import Dash_Rune
from scripts.entities.items.runes.random_runes.key_rune import Key_Rune

from scripts.entities.items.runes.fire_runes.fire_resistance_rune import Fire_Resistance_Rune
from scripts.entities.items.runes.fire_runes.fire_circle_rune import Fire_Circle_Rune
from scripts.entities.items.runes.fire_runes.fire_ball_rune import Fire_Ball_Rune
from scripts.entities.items.runes.fire_runes.fire_spray_rune import Fire_Spray_Rune

from scripts.entities.items.runes.freeze_runes.frozen_resistance_rune import Frozen_Resistance_Rune
from scripts.entities.items.runes.freeze_runes.freeze_circle_rune import Freeze_Circle_Rune
from scripts.entities.items.runes.freeze_runes.freeze_storm_rune import Freeze_Storm_Rune
from scripts.entities.items.runes.freeze_runes.freeze_spray_rune import Freeze_Spray_Rune
from scripts.entities.items.runes.freeze_runes.freeze_ball_rune import Freeze_Ball_Rune

from scripts.entities.items.runes.poison_runes.poison_resistance_rune import Poison_Resistance_Rune
from scripts.entities.items.runes.poison_runes.poison_ball_rune import Poison_Ball_Rune
from scripts.entities.items.runes.poison_runes.poison_cloud_rune import Poison_Cloud_Rune
from scripts.entities.items.runes.poison_runes.poison_plume_rune import Poison_Plume_Rune

from scripts.entities.items.runes.electric_runes.electric_ball_rune import Electric_Ball_Rune
from scripts.entities.items.runes.electric_runes.electric_spray_rune import Electric_Spray_Rune
from scripts.entities.items.runes.electric_runes.chain_lightning_rune import Chain_Lightning_Rune


from scripts.entities.items.runes.vampiric_runes.soul_reap_rune import Soul_Reap_Rune
from scripts.entities.items.runes.vampiric_runes.soul_pit_rune import Soul_Pit_Rune

from scripts.entities.items.runes.passive_runes.regen_rune import Regen_Rune


from scripts.entities.items.runes.constant_runes.light_rune import Light_Rune
from scripts.entities.items.runes.constant_runes.arcane_conduit_rune import Arcane_Conduit_Rune
from scripts.entities.items.runes.basic_runes.resistance_rune import Resistance_Rune
from scripts.entities.items.runes.constant_runes.shield_rune import Shield_Rune
from scripts.entities.items.runes.constant_runes.arcane_hunger_rune import Arcane_Hunger_Rune
from scripts.entities.items.runes.constant_runes.manget_rune import Magnet_Rune
from scripts.engine.keys.keys import keys
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.utility.luck_calculator import Luck_Calculator
import random

class Rune_Handler(Loot_Types_Handler):
    def __init__(self, game, item_handler):
        super().__init__(game)
        self.item_handler = item_handler
        self.active_runes = []
        self.saved_data = {}
        self.Configure_Rune_Tables()

        
        # Pre-calculate min cost for the base class performance
        self.min_cost = min(self.loot_types_cost.values())

    # Function to initialise the runes at the start of game
    # Gets 3 random runes with a value less than 30, then adds upgrades to
    # be roughly 100
    def Initialise_Runes(self):
        initial_runes = self.Get_Initial_Runes()
        for rune in initial_runes:
            value = self.loot_types_cost.get(rune)
            upgrades = 8
            rune = self.Loot_Spawner((999, 999), rune, value, upgrades)
            self.Add_Rune_To_Rune_Inventory(rune)


    # Returns a list containing only the keys where cost < 30
    def Get_Initial_Runes(self):
        runes_under_30 = [rune for rune, cost in self.loot_types_cost.items() if cost < 30]
        initial_runes = random.sample(runes_under_30, 2) # Select 3 random ones
        initial_runes.append(keys.freeze_spray_rune)
        return initial_runes
            

    def Load_Data(self, data):
        if not data:
            return None
        
        rune_type = data.get(keys.type)
        if not rune_type:
            return None

        pos = data[keys.pos]
        type = data[keys.type]
        amount = data[keys.amount]
        rarity_value = self.loot_types_cost.get(type)

        rune = self.Loot_Spawner(pos, rune_type, rarity_value, amount)
        if rune:
            rune.Load_Data(data)

        return rune
    
    def Save_Rune_Data(self):
        self.saved_data.clear()

        for rune in self.active_runes:
            self.saved_data[rune.ID] = rune.Save_Data()

        return self.saved_data

    
    # --- MODIFICATION LOGIC ---

    # Swaps an active rune for a new one
    def Replace_Rune_In_Inventory(self, old_rune, new_rune):
        # 1. Update Inventory System
        self.game.inventory.Replace_Rune(old_rune, new_rune)
        
        # 2. Activate New
        new_rune.active = True
        self.active_runes.append(new_rune)
        self.item_handler.Add_Item(new_rune)

        # 3. Deactivate Old
        old_rune.active = False
        if old_rune in self.active_runes:
            self.active_runes.remove(old_rune)
        self.item_handler.Remove_Item(old_rune)

    def Clear_Runes(self):
        self.active_runes.clear()
        self.saved_data.clear()

    def Remove_Rune_From_Active_Runes(self, rune):
        if rune not in self.active_runes:
            return False
        self.active_runes.remove(rune)
        return True


    # --- INVENTORY LOGIC ---

    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = 1):
        rune = super().Loot_Spawner(pos, type, rarity_value, amount)
        return rune

    def Add_Rune_To_Rune_Inventory(self, rune):
        if not rune:
            return
        self.item_handler.Add_Item(rune)
        rune.Pick_Up()
        self.active_runes.append(rune)
        return rune

    def Find_Nearby_Runes(self, entity_pos, max_distance):
        # Optimization: Use squared distance to avoid math.sqrt()
        scroll_x, scroll_y = self.game.render_scroll
        screen_pos = (entity_pos[0] - scroll_x, entity_pos[1] - scroll_y)
        
        max_dist_sq = max_distance ** 2
        return [r for r in self.active_runes if 
                (screen_pos[0] - r.pos[0])**2 + (screen_pos[1] - r.pos[1])**2 < max_dist_sq]

    def Check_If_Player_Has_Damage_Runes(self):
        return any(rune.type in self.damage_runes for rune in self.active_runes)

    def Update(self, delta_time):
        for rune in self.active_runes:
            rune.Update(delta_time)

    def Render_Animation(self, surf, offset=(0, 0)):
        for rune in self.active_runes:
            if not rune:
                print(self.active_runes)
                return
            rune.Render_Animation(surf, offset)

    def Get_Active_Runes(self):
        return self.active_runes

    def Configure_Rune_Tables(self):
        
        self.loot_map = {
            keys.dash_rune: Dash_Rune,
            keys.key_rune: Key_Rune,
            keys.regen_rune: Regen_Rune,
            keys.healing_rune: Healing_Rune,
            keys.invisibility_rune: Invisibility_Rune,
            keys.invulnerable_rune: Invulnerable_Rune,
            keys.resistance_rune: Resistance_Rune,
            keys.silence_rune: Silence_Rune,
            keys.speed_rune: Speed_Rune,
            keys.increase_strength_rune: Strength_Rune,
            keys.vampiric_rune: Vampiric_Rune,
            keys.arcane_conduit_rune: Arcane_Conduit_Rune,
            keys.arcane_hunger_rune: Arcane_Hunger_Rune,
            keys.light_rune: Light_Rune,
            keys.magnet_rune: Magnet_Rune,
            keys.shield_rune: Shield_Rune,
            keys.fire_resistance_rune: Fire_Resistance_Rune,
            keys.fire_cirlce_rune: Fire_Circle_Rune,
            keys.fire_ball_rune: Fire_Ball_Rune,
            keys.fire_spray_rune: Fire_Spray_Rune,
            keys.freeze_circle_rune: Freeze_Circle_Rune,
            keys.freeze_storm_rune: Freeze_Storm_Rune,
            keys.freeze_spray_rune: Freeze_Spray_Rune,
            keys.freeze_ball_rune: Freeze_Ball_Rune,
            keys.frozen_resistance_rune: Frozen_Resistance_Rune,
            keys.poison_resistance_rune: Poison_Resistance_Rune,
            keys.poison_ball_rune: Poison_Ball_Rune,
            keys.poison_cloud_rune: Poison_Cloud_Rune,
            keys.poison_plume_rune: Poison_Plume_Rune,
            keys.electric_ball_rune: Electric_Ball_Rune,
            keys.electric_spray_rune: Electric_Spray_Rune,
            keys.chain_lightning_rune: Chain_Lightning_Rune,
            keys.soul_reap_rune: Soul_Reap_Rune,
            keys.soul_pit_rune: Soul_Pit_Rune,
        }

        self.loot_types_cost = {
            # Utility & Movement
            keys.dash_rune : 10,                # Dash
            keys.key_rune : 15,                 # Door unlock
            keys.regen_rune : 30,               # Regen (Passive)

            # Buffs & Survival
            keys.healing_rune : 20,             # Healing
            keys.invisibility_rune : 60,        # Invisibility
            keys.invulnerable_rune: 45,         # Immunity
            keys.resistance_rune : 40,          # General damage resistance
            keys.silence_rune : 55,             # Active Silence effect
            keys.speed_rune : 15,               # Active Speed effect
            keys.increase_strength_rune : 15,   # Active Strength effect
            keys.vampiric_rune : 25,            # Vampiric, regen from damaging enemies

            # Passive Runes
            keys.arcane_conduit_rune : 40,      # Arcane conduit, increase power level of your other runes
            keys.arcane_hunger_rune : 30,       # Arcane Hunger, increase souls generation
            keys.light_rune : 15,               # Passive light
            keys.magnet_rune : 10,              # Magnet, Auto pickup of items
            keys.shield_rune : 15,              # Frost Shield, enemies freeze when damaging you (or general shield)


            # Fire Runes
            keys.fire_resistance_rune : 10,     # Passive Fire Resistance
            keys.fire_cirlce_rune : 20,         # Fire wall, wall of fire that damage anything that tries to cross it
            keys.fire_ball_rune : 35,           # Fireball, ball of fire that leads to fire explosion
            keys.fire_spray_rune : 15,          # Fire spew, flamethrower attack

            # Frost Runes
            keys.freeze_circle_rune : 30,       # Area freeze effect
            keys.freeze_storm_rune : 30,        # Ice storm, Creates a tornado that shoots ice projectiles
            keys.freeze_spray_rune : 15,        # Ice projectiles, fast ice projectiles shot like a bullet
            keys.freeze_ball_rune : 35,         # Iceball, ball that causes a freeze explosion
            keys.frozen_resistance_rune : 10,   # Passive Frost Resistance

            # Poison Runes
            keys.poison_resistance_rune : 10,   # Passive Poison Resistance
            keys.poison_ball_rune : 25,         # Poison ball that turns into a poison cloud
            keys.poison_cloud_rune : 30,        # Poison cloud, creates a big poison cloud around entity (AoE)
            keys.poison_plume_rune : 20,        # Poison plumes, creates poison clouds at random positions

            # Electric Runes
            keys.electric_ball_rune : 25,       # Electric ball that generates electric explosion
            keys.electric_spray_rune : 20,      # Electric homing particle, target nearest entity
            keys.chain_lightning_rune : 35,     # Chain lightning, Lightning projectile that bounces

            # Vampiric Runes
            keys.soul_reap_rune : 25,           # Soul reap, broad projectile that sucks health
            keys.soul_pit_rune : 30,            # Soul pit that pulls entities in and sucks health

        } 

        self.damage_runes = {
            keys.fire_ball_rune, keys.fire_spray_rune, keys.freeze_storm_rune,
            keys.freeze_spray_rune, keys.freeze_ball_rune, keys.poison_ball_rune,
            keys.poison_cloud_rune, keys.poison_plume_rune, keys.electric_ball_rune,
            keys.electric_spray_rune, keys.chain_lightning_rune, keys.soul_reap_rune,
            keys.soul_pit_rune,
        }