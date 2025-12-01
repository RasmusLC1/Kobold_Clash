from scripts.entities.items.loot.valueable.valueable import Valuable
from scripts.engine.keys.keys import keys

class Gem(Valuable):
    def __init__(self, game, pos, amount, effect, value):
        self.effect = effect
        super().__init__(game, effect + '_' + keys.gem, pos, value=value, amount=amount, max_amount = 10)
        self.type = keys.gem
        self.max_amount = 10 # Amount acts as damage, each extra amount = 1 * strength damage
        


    def Set_Description(self):
        print(self.amount)
        self.description = f"Add {self.effect, self.amount}\nto weapon\ngold {self.Calculate_Value()}\n"