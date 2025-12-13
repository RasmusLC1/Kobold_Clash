from scripts.entities.items.loot.gems_ingots.gem import Gem
from scripts.entities.items.loot.gems_ingots.ingot import Ingot
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
            keys.ingot: Ingot,
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
        print(sub_type, loot_type)
        return loot_type


    def Get_Loot_Values(self):
        gems_and_ingots = {
            # keys.fire_gem: 10,        # Set fire effect on weapon
            # keys.frozen_gem: 10,      # Set freeze effect on weapon
            # keys.electric_gem: 10,    # Set electric effect on weapon
            # keys.poison_gem: 10,      # Set poison effect on weapon
            # keys.vampiric_gem: 30,    # Set vampiric effect on weapon
            # keys.arcane_hunger_gem: 30,   # Set Arcane hunger effect on weapon
            # keys.blunt_gem: MIN_GEM_VALUE,  # Set blunt damage on weapon
            # keys.slash_gem: MIN_GEM_VALUE,  # Set slash damage on weapon
            # keys.halo_gem: 40,        # Grants wielder a chance to protect from damage
            # keys.power_gem: 30,       # Increases rune power while equipped
            # keys.range_gem: 10,       # Increases weapon range
            # keys.speed_gem: 10,       # Increases weapon attack speed
            # keys.strength_gem: 10,    # Increases wielders strength
            # keys.terror_gem: 40,      # Chance for enemies to run away
            # keys.vulnerable_gem: 20,  # Entities hit take extra damage
            # keys.weakness_gem: 20,    # Entities hit gets weakness
            # keys.wet_gem: 10,         # Set wet effect on weapon, can combo
            # keys.durability_gem: 10,  # Increases weapon health
            # # keys.multishot: 50,       # Fires two arrows at a time (guessed cost 50)

            keys.Steel_ingot: 15,     # Repairs weapons
            keys.jade_ingot: 15,      # Repairs runes
            keys.copper_ingot: 20,    # Add amount to utility items
            keys.Gold_ingot: 30,      # Can add gem slots
            keys.Silver_ingot: 30,    # Can upgrade rune power
        }
        return gems_and_ingots

