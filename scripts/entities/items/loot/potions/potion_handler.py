from scripts.entities.items.loot.potions.potion import Potion
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.utility.luck_calculator import Luck_Calculator

from scripts.engine.keys.keys import keys


class Potion_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

    def Get_Strength(self, key):
        strength = {
            keys.healing: 20,
            keys.regen: 4,
            keys.increase_souls: 20,
            keys.speed: 4,
            keys.increase_strength: 4,
            keys.invisibility: 3,
            keys.silence: 3,
            keys.fire_resistance: 6,
            keys.frozen_resistance: 6,
            keys.poison_resistance: 6,
            keys.vampiric: 5,
            keys.arcane_hunger: 5,
        }

        return strength.get(key, 1)


    def Get_Loot_Values(self):
        loot_types_cost = {
            keys.healing: 20,
            keys.regen: 20,
            keys.increase_souls: 10,
            keys.speed: 10,
            keys.increase_strength: 10,
            keys.invisibility: 70,
            keys.silence: 60,
            keys.fire_resistance: 10,
            keys.frozen_resistance: 10,
            keys.poison_resistance: 10,
            keys.vampiric: 50,
            keys.arcane_hunger: 50,
        }

        # Adjust the cost based on player state
        player = self.game.player
        loot_types_cost = self.Adjust_By_Player_Health(loot_types_cost, player)
        loot_types_cost = self.Adjust_By_Souls(loot_types_cost, player)
        return loot_types_cost


    def Adjust_By_Souls(self, weights, player):
        max_amount = 300
        if player.souls > max_amount:
            return weights
        
        soul_increase = max_amount - player.souls
        
        # Normalise from 0 to 10
        normalized = (soul_increase / max_amount) * 10

        weights[keys.increase_souls] += normalized 
        weights[keys.arcane_hunger] += normalized

        return weights


    # Adjust the drop chance of healing potions if the players health is low
    def Adjust_By_Player_Health(self, weights, player):
        missing = player.max_health - player.health

        # Normalize missing health to 0–20
        normalized = (missing / player.max_health) * 20

        if normalized <= 0:
            return weights

        weights[keys.healing]  += normalized
        weights[keys.regen]    += normalized
        weights[keys.vampiric] += normalized

        return weights


    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = None):
        if not type:   
            type, amount = Luck_Calculator.Get_Loot_Based_On_Rarity(rarity_value, self.Get_Loot_Values())

        strength = self.Get_Strength(type)
        potion = Potion(self.game, type, pos, amount, strength)

        self.game.item_handler.Add_Item(potion)
        
        return potion


    def Spawn_Potions(self, name, pos_x, pos_y, amount, data=None):
        name = name.replace("_", keys.potion, "")
        # potion_class = self.potion_map.get(name)

        # If none matched, return False
        if name not in self.potions:
            return None

        # Instantiate the matched potion class
        potion = Potion(self.game, name, (pos_x, pos_y), amount, self.strength[name])
        # Load any saved data if present
        if data:
            potion.Load_Data(data)

        # Finally, add the potion to the game’s item handler
        self.game.item_handler.Add_Item(potion)
        return potion