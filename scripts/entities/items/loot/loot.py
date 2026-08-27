from scripts.entities.items.item import Item
from scripts.entities.textbox.loot_textbox import Loot_Textbox
from scripts.engine.keys.keys import keys

class Loot(Item):
    def __init__(self, game, type, pos, size, rarity_value, loot_type,
                 amount = 1, max_amount = 1, max_animation = 0,
                 animation_cooldown_max=0):
        super().__init__(game=game, type=type, sub_category=keys.loot, pos=pos,
                         size=size, amount=amount, add_to_tile=True,
                           rarity_value = rarity_value, max_amount=max_amount,
                           max_animation=max_animation,
                            animation_cooldown_max=animation_cooldown_max)
        self.loot_type =  loot_type
        self.Set_Description()

    def Save_Data(self):
        super().Save_Data()
        self.saved_data[keys.loot_type] = self.loot_type

    def Load_Data(self, data):
        # self.type = data[keys.type]
        self.loot_type = data[keys.loot_type]
        super().Load_Data(data)

    def Update_Animation(self, delta_time = 0):
        pass

    def Set_Description(self):
        self.description = f"{self.Calculate_Value()} {keys.gold}\n"

    def Revive(self):
        return False
    

    def Set_Text_Box(self):
        self.text_box = Loot_Textbox(self)
