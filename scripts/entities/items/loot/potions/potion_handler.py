from scripts.entities.items.loot.potions.potion import Potion
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.utility.luck_calculator import Luck_Calculator

from scripts.engine.keys.keys import keys


class Potion_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)

        # Static Strengths
        self.potion_strengths = {
            keys.healing: 20,
            keys.regen: 4,
            keys.increase_souls: 20,
            keys.speed: 3,
            keys.increase_strength: 3,
            keys.invisibility: 3,
            keys.silence: 3,
            keys.fire_resistance: 5,
            keys.frozen_resistance: 5,
            keys.poison_resistance: 5,
            keys.vampiric: 3,
            keys.arcane_hunger: 2,
            keys.luck: 2,
        }

        # Base Costs Template
        self.base_loot_costs = {
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
            keys.luck: 20,
        }

    def Get_Strength(self, key):
        # Instant lookup with a default value of 1
        return self.potion_strengths.get(key, 1)

    def Get_Loot_Values(self):
        # Use copy to prevent the base values from being permanently altered
        loot_types_cost = self.base_loot_costs.copy()

        # Adjust the copy based on player state
        player = self.game.player
        self.Adjust_By_Player_Health(loot_types_cost, player)
        self.Adjust_By_Souls(loot_types_cost, player)
        
        return loot_types_cost

    def Adjust_By_Souls(self, weights, player):
        max_amount = 300
        if player.souls < max_amount:
            soul_increase = max_amount - player.souls
            normalized = (soul_increase / max_amount) * 10
            
            weights[keys.increase_souls] += normalized 
            weights[keys.arcane_hunger] += normalized


    def Adjust_By_Player_Health(self, weights, player):
        missing = player.max_health - player.health
        if missing <= 0:
            return

        normalized = (missing / player.max_health) * 20
        weights[keys.healing]  += normalized
        weights[keys.regen]    += normalized
        weights[keys.vampiric] += normalized