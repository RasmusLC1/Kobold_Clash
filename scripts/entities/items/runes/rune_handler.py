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

import math

class Rune_Handler():
    def __init__(self, game):
        self.game = game
        self.active_runes = []
        self.saved_data = {}
        self.runes = {}
        self.Rune_Spawner()
    

    def Save_Rune_Data(self):
        for rune in self.active_runes:
            self.saved_data[rune.type] = rune.Save_Data()

        return self.saved_data
    
    
    def Load_Data(self, data):
        if not data:
            return None
        
        type = data.get(keys.type)

        if not type:
            return None
        rune = self.Add_Rune_To_Rune_Inventory(type)
        if not rune:
            print("ERROR LOADING RUNE RUNEHANDLER", rune, type)
            return None
        
        rune.Load_Data(data)
        self.active_runes.append(rune)

        return rune

    
    def Update(self, offset = (0,0)):
        for rune in self.active_runes:
            rune.Update()
    
    def Initialise_Runes(self):
        self.Add_Runes_To_Inventory_TEST()

    def Rune_Spawner(self):
        self.runes = {
            keys.dash_rune : Dash_Rune,
            keys.key_rune : Key_Rune,
            keys.regen_rune : Regen_Rune,

            keys.healing_rune : Healing_Rune,
            keys.invisibility_rune : Invisibility_Rune,
            keys.invulnerable_rune: Invulnerable_Rune,
            keys.resistance_rune : Resistance_Rune,
            keys.silence_rune : Silence_Rune,
            keys.speed_rune : Speed_Rune,
            keys.increase_strength_rune : Strength_Rune,
            keys.vampiric_rune : Vampiric_Rune,

            keys.arcane_conduit_rune : Arcane_Conduit_Rune,
            keys.arcane_hunger_rune : Arcane_Hunger_Rune,
            keys.light_rune : Light_Rune,
            keys.magnet_rune : Magnet_Rune,
            keys.shield_rune : Shield_Rune,

            keys.fire_resistance_rune : Fire_Resistance_Rune,
            keys.fire_cirlce_rune : Fire_Circle_Rune,
            keys.fire_ball_rune : Fire_Ball_Rune,
            keys.fire_spray_rune : Fire_Spray_Rune,
            
            keys.freeze_circle_rune : Freeze_Circle_Rune,
            keys.freeze_storm_rune : Freeze_Storm_Rune,
            keys.freeze_spray_rune : Freeze_Spray_Rune,
            keys.freeze_ball_rune : Freeze_Ball_Rune,
            keys.frozen_resistance_rune : Frozen_Resistance_Rune,
            
            keys.poison_resistance_rune : Poison_Resistance_Rune,
            keys.poison_ball_rune : Poison_Ball_Rune,
            keys.poison_cloud_rune : Poison_Cloud_Rune,
            keys.poison_plume_rune : Poison_Plume_Rune,

            keys.electric_ball_rune : Electric_Ball_Rune,
            keys.electric_spray_rune : Electric_Spray_Rune,
            keys.chain_lightning_rune : Chain_Lightning_Rune,

            keys.soul_reap_rune : Soul_Reap_Rune,
            keys.soul_pit_rune : Soul_Pit_Rune,

        }

        self.damage_runes = [
            # keys.fire_cirlce_rune,
            keys.fire_ball_rune,
            keys.fire_spray_rune,
            # keys.freeze_circle_rune,
            keys.freeze_storm_rune,
            keys.freeze_spray_rune,
            keys.freeze_ball_rune,
            keys.poison_resistance_rune,
            keys.poison_ball_rune,
            keys.poison_cloud_rune,
            keys.poison_plume_rune,
            keys.electric_ball_rune,
            keys.electric_spray_rune,
            keys.chain_lightning_rune,
            keys.soul_reap_rune,
            keys.soul_pit_rune,
        ]



    def Add_Runes_To_Inventory_TEST(self):
        self.Add_Rune_To_Rune_Inventory(keys.key_rune)
        self.Add_Rune_To_Rune_Inventory(keys.fire_spray_rune)
        self.Add_Rune_To_Rune_Inventory(keys.dash_rune)


    def Clear_Runes(self):
        self.runes.clear()
        self.active_runes.clear()
        self.saved_data.clear()
    
    def Replace_Rune_In_Inventory(self, old_rune, new_rune):
        self.game.inventory.Replace_Rune(old_rune, new_rune)
        new_rune.active = True
        self.active_runes.append(new_rune)

        self.game.item_handler.Add_Item(new_rune)

        old_rune.active = False
        self.active_runes.remove(old_rune)
        self.game.item_handler.Remove_Item(old_rune)


    def Spawn_Rune_Floor(self, rune_type, pos):
        rune_class = self.runes.get(rune_type)
        if not rune_class:
            print(rune_type, rune_class)
            return
        
        rune = rune_class(self.game, pos)
        self.game.item_handler.Add_Item(rune)
        rune.Set_Tile()




    # Add runes to Active Inventory
    def Add_Rune_To_Rune_Inventory(self, rune_type):
        rune_class = self.runes.get(rune_type)
        if not rune_class:
            print(rune_type)
            return None
        
        rune = rune_class(self.game, (999, 999))
        rune.active = True
        self.active_runes.append(rune)
        self.game.item_handler.Add_Item(rune)
        rune.Pick_Up()
        return rune

    # Only one of each rune, so easy filter by rune_type return when found
    def Remove_Rune_From_Inventory(self, rune_type):
        rune = self.runes[rune_type]
        
        rune.active = False
        self.active_runes.remove(rune)
        self.game.inventory.Update_Runes()
        self.game.item_handler.Remove_Item(rune)

        return True
    
    def Remove_Rune_From_Active_Runes(self, rune):
        if not rune in self.active_runes:
            print(self.active_runes)
            return
        self.active_runes.remove(rune)
    
    def Get_Rune(self, type):
        return self.runes[type]
    
    def Find_Nearby_Runes(self, entity_pos, max_distance):
        entity_pos = (entity_pos[0] - self.game.render_scroll[0], entity_pos[1] - self.game.render_scroll[1])
        nearby_runes = []
        for rune in self.active_runes:
            # Calculate the Euclidean distance
            distance = math.sqrt((entity_pos[0] - rune.pos[0]) ** 2 + (entity_pos[1] - rune.pos[1]) ** 2)
            if distance < max_distance:
                nearby_runes.append(rune)

        return nearby_runes
        
    def Check_If_Player_Has_Damage_Runes(self):
        for rune in self.active_runes:
            if rune.type in self.damage_runes:
                return True
            
        return False
    
    def Check_If_Rune_Is_Active(self, new_rune_type):
        for active_rune in self.active_runes:
            if active_rune.type == new_rune_type:
                return True
        return False

    def Render_Animation(self, surf, offset = (0, 0)):
        for rune in self.active_runes:
            rune.Render_Animation(surf, offset)


