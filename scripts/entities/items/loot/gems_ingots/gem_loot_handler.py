from scripts.entities.items.loot.gems_ingots.gem import Gem
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys
from scripts.engine.utility.luck_calculator import Luck_Calculator

MIN_GEM_VALUE = 5


class Gem_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

        self.loot_types_cost = {
            keys.fire_gem: 10,
            keys.frozen_gem: 10,
            keys.electric_gem: 10,
            keys.poison_gem: 10,
            keys.vampiric_gem: 30,
            keys.arcane_hunger_gem: 30,
            keys.blunt_gem: MIN_GEM_VALUE,
            keys.slash_gem: MIN_GEM_VALUE,
            keys.halo_gem: 40,
            keys.power_gem: 30,
            keys.range_gem: 10,
            keys.speed_gem: 10,
            keys.strength_gem: 10,
            keys.terror_gem: 40,
            keys.vulnerable_gem: 20,
            keys.weakness_gem: 20,
            keys.wet_gem: 10,
            keys.durability_gem: 10,
        }

        # Every gem type is spawned by the same class
        self.loot_map = {gem_type: Gem for gem_type in self.loot_types_cost}

    def Get_Random_Gem(self, rarity_value):
        gem_type, amount, value = Luck_Calculator.Get_Loot_Based_On_Rarity(
            rarity_value, self.Get_Loot_Values())
        return gem_type, value