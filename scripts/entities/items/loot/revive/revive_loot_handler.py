from scripts.entities.items.loot.revive.phoenix_feather import Phoenix_Feather
from scripts.entities.items.loot.revive.light_pendant import Light_Pendant
from scripts.entities.items.loot.revive.gravediggers_coin import Gravediggers_Coin
from scripts.entities.items.loot.revive.blood_pact import Blood_Pact 
from scripts.entities.items.loot.loot_types_handler import Loot_Types_Handler
from scripts.engine.keys.keys import keys


class Revive_Loot_Handler(Loot_Types_Handler):
    def __init__(self, game):
        super().__init__(game)
 

        self.loot_map = {
            keys.phoenix_feather: Phoenix_Feather,
            keys.light_pendant: Light_Pendant,
            keys.blood_pact: Blood_Pact,
            keys.gravediggers_coin: Gravediggers_Coin,
        }

 
    
    def Get_Loot_Values(self):
        loot_types_cost = {
            # Phoenix Feather – Upon death, revives the player with 1 health, then burns up.
            keys.phoenix_feather: 45,
            
            # Pendant of light, Revive on death for souls 
            keys.light_pendant: 40,

            # Gravedigger’s Coin – Revive the player one time to full health for gold
            keys.gravediggers_coin: 45,

            # Blood Pact Scroll – Allows revival at the cost of a permanent debuff.
            keys.blood_pact : 30
        }

        return loot_types_cost


