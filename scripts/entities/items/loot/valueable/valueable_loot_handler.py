from scripts.entities.items.loot.valueable.gold import Gold
from scripts.entities.items.loot.valueable.gem import Gem
from scripts.entities.items.loot.valueable.hunter_treasure import Hunter_Treasure 
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys
import random



class Valuable_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)


        self.loot_map = {
            keys.gold: self.Spawn_Gold,
            keys.gem: self.Spawn_Gem,
            keys.hunter_treasure: self.Spawn_Hunter_Treasure
        }

    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = 0):
        if not type:
            type, amount = self.Get_Loot_Based_On_Rarity(rarity_value)

        if str(type).endswith("_gem"):
            loot_class = self.Spawn_Gem
        else:
            loot_class = self.loot_map.get(type)

        if not loot_class:
            return None

        loot = loot_class(pos, int(amount), type)

        self.game.item_handler.Add_Item(loot)
        return loot



    def Spawn_Gold(self, pos, amount = None, type = None):
        if not amount:
            amount = random.randint(5 * self.game.level, 15 * self.game.level)


        loot = Gold(self.game, pos, amount)
        return loot

    
    def Spawn_Gem(self, pos, amount, type):

        effect = type.split("_g")[0] # Use _g to prevent failure at multi word gems like increase_strength
        loot_types_cost = self.Get_Loot_Values()
        value = loot_types_cost.get(type, 10)
        loot = Gem(self.game, pos, amount, effect, value)
        return loot

    def Spawn_Hunter_Treasure(self, pos, amount = 0, type = None):
        loot = Hunter_Treasure(self.game, pos)
        return loot


    def Get_Loot_Values(self):
        loot_types_cost = {
            keys.gold : 10,
            keys.fire_gem : 10,
            keys.frozen_gem : 10,
            keys.electric_gem : 10,
            keys.poison_gem : 10,
            keys.vampiric_gem : 30,
            keys.arcane_hunger : 30,
            keys.blunt_gem : 5,
            keys.slash_gem : 5,
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
        return loot_types_cost
