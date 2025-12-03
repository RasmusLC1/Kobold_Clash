from scripts.entities.items.loot.gems_ingots.gem import Gem
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys
from scripts.engine.utility.luck_calculator import Luck_Calculator

MIN_GEM_VALUE = 5

# Handle valuables uniquely since gems and ingots have a large pool of potential items
class Gem_Ingot_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

        self.loot_map = {
            keys.gem: Gem,
        }

    def Loot_Spawner(self, pos, sub_type = None, rarity_value = 0, amount = None):
        if not sub_type:
            sub_type, amount = Luck_Calculator.Get_Loot_Based_On_Rarity(rarity_value, self.Get_Loot_Values())
        

        loot_type = self.Get_Type(sub_type)
        if not loot_type:
            return None

        loot_class = self.loot_map.get(loot_type)
        if not loot_class:
            return None

        try:
            loot = loot_class(self.game, sub_type, pos, amount, rarity_value)
            self.game.item_handler.Add_Item(loot)
        except Exception as e:
            print(f"Failed to spawn loot{e}", sub_type, pos, amount, rarity_value, loot_class)
            return

        return loot

    # Get the actual parent type from the dictionary
    def Get_Type(self, sub_type):
        loot_type = None
        if keys.gem in sub_type:
            loot_type = keys.gem
        elif keys.ingot in sub_type:
            loot_type = keys.ingot 

        return loot_type


    def Get_Loot_Values(self):
        gems = {
            keys.fire_gem : 10,
            keys.frozen_gem : 10,
            keys.electric_gem : 10,
            keys.poison_gem : 10,
            keys.vampiric_gem : 30,
            keys.arcane_hunger : 30,
            keys.blunt_gem : MIN_GEM_VALUE,
            keys.slash_gem : MIN_GEM_VALUE,
            keys.halo_gem : 40,
            keys.power_gem : 30,
            keys.range_gem : 10,
            keys.speed_gem : 10,
            keys.strength_gem : 10,
            keys.terror_gem : 40,
            keys.vulnerable_gem : 20,
            keys.weakness_gem : 20,
            keys.wet_gem : 10,
            keys.durability_gem : 10,
        }
        return gems

