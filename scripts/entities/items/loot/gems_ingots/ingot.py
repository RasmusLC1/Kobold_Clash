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
            keys.Silver_ingot : f"Add {self.amount} power\nto rune",
        }
        self.description = descriptions.get(self.sub_type)+f"\nvalue:\t{self.Calculate_Value()} {keys.gold}"


    def Add_Ingot_To_Item(self, item):
        functions = {
            keys.Steel_ingot : self.Increase_Durability(), 
            keys.jade_ingot : self.Increase_Durability(), 
            keys.copper_ingot : self.Increase_Item_Amount(),
            keys.Gold_ingot : self.Add_Gem_Slot_To_Item(),
            keys.Silver_ingot : self.Add_Gem_Slot_To_Item(),
        }
        function = functions.get(item.type)
        function(item)
        self.Decrease_Amount(1)

    def Increase_Durability(self, item):
        durability_tenth = int(max(1, item.max_durability // 10))
        item.Increase_Durability(durability_tenth)

    def Increase_Item_Amount(self, item):
        amount_tenth = int(max(1, item.max_amount // 10))
        item.Increase_Max_Amount(amount_tenth)
        item.Increase_Amount(amount_tenth)

    def Add_Gem_Slot_To_Item(self, item):
        item.Increase_Power(1)