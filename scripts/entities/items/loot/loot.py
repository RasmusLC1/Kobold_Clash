from scripts.entities.items.item import Item
from scripts.entities.textbox.loot_textbox import Loot_Textbox
from scripts.engine.keys.keys import keys

class Loot(Item):
    def __init__(self, game, type, pos, size, rarity_value, loot_type, amount = 1, max_amount = 1, max_animation=0):
        super().__init__(game=game, type=type, sub_category=keys.loot, pos=pos, size=size, amount=amount, add_to_tile=True, rarity_value = rarity_value, max_amount=max_amount, max_animation=max_animation)
        self.loot_type =  loot_type
        self.Set_Description()
        self.text_box = Loot_Textbox(self)

    def Save_Data(self):
        # self.saved_data[keys.type] = self.type
        self.saved_data[keys.loot_type] = self.loot_type
        super().Save_Data()

    def Load_Data(self, data):
        # self.type = data[keys.type]
        self.loot_type = data[keys.loot_type]
        super().Load_Data(data)

    def Update_Animation(self, delta_time = 0):
        pass

    def Set_Description(self):
        self.description = f"gold {self.value}\n"

    def Revive(self):
        return False
    
