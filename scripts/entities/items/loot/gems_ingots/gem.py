from scripts.entities.items.loot.valueable.valueable import Valuable
from scripts.engine.keys.keys import keys

class Gem(Valuable):

    def __init__(self, game, gem_name, pos, amount, rarity_value):

         # Use _g to prevent failure at multi word gems like increase_strength
        self.effect = gem_name.split("_g")[0]
        super().__init__(game, type=gem_name, pos=pos, value=rarity_value, amount=amount, max_amount = 10)
        self.type = keys.gem
        


    def Set_Description(self):
        self.description = f"Add {self.effect, self.amount}\nto weapon\n{self.Calculate_Value()} {keys.gold}\n"