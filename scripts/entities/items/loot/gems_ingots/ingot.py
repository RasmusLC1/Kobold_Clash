from scripts.entities.items.loot.valueable.valueable import Valuable
from scripts.engine.keys.keys import keys

# TODO: FUNCTIONALITY NEEDS TO BE IMPLEMENTED
class Ingot(Valuable):

    def __init__(self, game, ingot_name, pos, amount, rarity_value):

        super().__init__(game, type=ingot_name, pos=pos, value=rarity_value, amount=amount, max_amount = 10)
        self.type = keys.ingot

    def Set_Description(self):
        descriptions = {
            keys.Steel_ingot : f"Repairs weapons\nby {self.amount}",
            keys.jade_ingot : f"Repairs Runes\nby {self.amount}",
            keys.copper_ingot : f"Add amount\nto items {self.amount}",
            keys.Gold_ingot : f"Add {self.amount} gemslots\nto weapon",
            keys.Silver_ingot : f"Add {self.amount} gemslots\nto rune",
        }
        self.description = descriptions.get(self.sub_type)+f"\nvalue:\t{self.Calculate_Value()} {keys.gold}"