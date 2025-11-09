from scripts.entities.items.loot.potions.potion import Potion
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler

import random
from scripts.engine.keys.keys import keys


class Potion_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)
        self.potions = [
            keys.healing,
            keys.regen,
            keys.vampiric,
            keys.increase_souls,
            keys.speed,
            keys.increase_strength,
            keys.invisibility,
            keys.silence,
            keys.fire_resistance,
            keys.frozen_resistance,
            keys.poison_resistance,
            keys.arcane_hunger,
        ]

        self.strength = {
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

        self.rarity = {
            keys.healing: keys.common,
            keys.regen: keys.rare,
            keys.increase_souls: keys.uncommon,
            keys.speed: keys.uncommon,
            keys.increase_strength: keys.common,
            keys.invisibility: keys.epic,
            keys.silence: keys.rare,
            keys.fire_resistance: keys.common,
            keys.frozen_resistance: keys.common,
            keys.poison_resistance: keys.common,
            keys.vampiric: keys.uncommon,
            keys.arcane_hunger: keys.uncommon,
        }

        self.weights = {
            keys.healing: 0.1,
            keys.regen: 0.1,
            keys.increase_souls: 0.2,
            keys.speed: 0.2,
            keys.increase_strength: 0.2,
            keys.invisibility: 0.05,
            keys.silence: 0.05,
            keys.fire_resistance: 0.15,
            keys.frozen_resistance: 0.15,
            keys.poison_resistance: 0.15,
            keys.vampiric: 0.1,
            keys.arcane_hunger: 0.1,
        }



    def Update_Potion_Weights(self):
        weights = self.weights.copy()
        player = self.game.player
        
        weights = self.Adjust_By_Player_Health(weights, player)
        weights = self.Adjust_By_Souls(weights, player)

        return weights
    
    def Adjust_By_Souls(self, weights, player):
        max_amount = 300
        if player.souls > max_amount:
            return weights
        
        soul_increase =( max_amount - player.souls) / 400
        weights[keys.increase_souls] += soul_increase 
        weights[keys.arcane_hunger] += soul_increase

        return weights


    # Adjust the drop chance of healing potions if the players health is low
    def Adjust_By_Player_Health(self, weights, player):
        player_health_missing = player.max_health - player.health
        if player_health_missing < 30:
            return weights
        

        player_health_missing /= 400
        weights[keys.healing] += player_health_missing
        weights[keys.regen] += player_health_missing
        weights[keys.vampiric] += player_health_missing

        return weights
    

    def Loot_Spawner(self, pos, type = None, rarity_value = 0, amount = None):
        if not type:   
            weights_dict = self.Update_Potion_Weights()
            
            # Extract weight values in the same order as potions list
            weight_values = [weights_dict[potion] for potion in self.potions]
            type = random.choices(self.potions, weight_values, k=1)[0]
        if not amount:
            amount = random.randint(1, 3)

        potion = Potion(self.game, type, pos, amount, self.strength[type])

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