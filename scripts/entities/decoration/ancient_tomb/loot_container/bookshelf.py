from scripts.entities.decoration.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys
import random

key_empty = 'empty'

class Bookshelf(Loot_Container):
    def __init__(self, game, pos) -> None:
        self.enemies = {}
        super().__init__(game, keys.bookshelf, pos, (32, 32))
        self.tile.Set_Physics(True) # Bookshelf is impassible


    def Set_Loot_Types(self):
        self.loot_weights = {keys.recipe_scroll : 0.1,
                             keys.temptress_embrace: 0.1,
                             keys.demonic_bargain: 0.1,
                             keys.blood_tomb: 0.1,
                             keys.recipe_scroll: 0.1,
                             keys.rune: 0.2,
                             key_empty : 1
                             }
        
        self.loot_categories = {
            keys.temptress_embrace : keys.curse,
            keys.demonic_bargain : keys.curse,
            keys.blood_tomb : keys.curse,
            keys.recipe_scroll : keys.passive,
        } 

    def Spawn_Loot(self, loot_type, pos):
        if loot_type == key_empty:
            return
        elif loot_type == keys.rune:
            self.Select_Available_Rune()
        else:
            loot_category = self.loot_categories[loot_type]
            self.game.item_handler.loot_handler.Spawn_Loot_Type(loot_category, pos, None, loot_type)
        return


    def Select_Available_Rune(self):
        # Get the rune object using the random key
        runes = self.Adjust_Rune_Weight()

        counter = 0
        rune_handler = self.game.rune_handler
        rune_type = None
        rune_active = False
        while not rune_active:
            rune_type = random.choices(
                    population=list(runes.keys()),
                    weights=list(runes.values()),
                    k=1
                )[0]
            counter += 1
            rune_active = rune_handler.Check_If_Rune_Is_Active(rune_type)
            if counter >= 20 or not rune_active:
                break

        if not rune_type:
            print("UNIQUE RUNE NOT FOUND BOOKSHELF")
            return self.Select_Available_Rune(keys.recipe_scroll, self.Get_Pos())
        
        self.Spawn_Rune(rune_type)
        return True

        
    def Spawn_Rune(self, rune_type):
        self.game.rune_handler.Spawn_Rune_Floor(rune_type, self.Get_Pos())
        return
    

    def Adjust_Rune_Weight(self):
        runes = {
            keys.dash_rune : 0.2,
            keys.key_rune : 0.1,
            keys.regen_rune : 0.1,

            keys.healing_rune : 0.2,
            keys.resistance_rune : 0.1,
            keys.speed_rune : 0.2,
            keys.increase_strength_rune : 0.2,
            keys.vampiric_rune : 0.2,

            keys.arcane_hunger_rune : 0.2,
            keys.light_rune : 0.4,
            keys.magnet_rune : 0.2,

            keys.fire_resistance_rune : 0.2,
            keys.fire_spray_rune : 0.1,
            
            keys.freeze_storm_rune : 0.1,
            keys.freeze_spray_rune : 0.1,
            keys.frozen_resistance_rune : 0.2,
            
            keys.poison_resistance_rune : 0.2,
            keys.poison_cloud_rune : 0.1,
            keys.poison_plume_rune : 0.1,

            keys.electric_spray_rune : 0.1,
            keys.chain_lightning_rune : 0.1,

            keys.soul_reap_rune : 0.1,
        }

        damage_runes = [
            keys.fire_resistance_rune,
            keys.fire_spray_rune,
            keys.freeze_storm_rune,
            keys.freeze_spray_rune,
            keys.frozen_resistance_rune,
            keys.poison_resistance_rune,
            keys.poison_cloud_rune,
            keys.poison_plume_rune,
            keys.electric_spray_rune,
            keys.chain_lightning_rune,
            keys.soul_reap_rune,
        ]

        if not self.game.rune_handler.Check_If_Player_Has_Damage_Runes():
            for damage_rune in damage_runes:
                if damage_rune in runes:
                    runes[damage_rune] += 0.1

        return runes
        
    

