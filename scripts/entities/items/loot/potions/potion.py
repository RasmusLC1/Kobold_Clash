from scripts.entities.items.loot.loot import Loot
from scripts.entities.textbox.potion_textbox import Potion_Textbox
from scripts.engine.keys.keys import keys

class Potion(Loot):
    def __init__(self, game, type, pos, amount, strength):
        super().__init__(game, type, pos, (16, 16), 5, keys.potion, amount)
        self.max_amount = 3
        self.max_animation = 4
        self.strength = strength
        
        self.text_box = Potion_Textbox(self)
        self.Set_Description()
    

    def Save_Data(self):

        super().Save_Data()
        self.saved_data['effect'] = self.effect
        self.saved_data['strength'] = self.strength

    def Load_Data(self, data):
        super().Load_Data(data)
        self.effect = data['effect']
        self.strength = data['strength']

    def Set_Description(self):
        self.description = (
                            f"{self.effect} {self.amount}\n"
                            f"gold {self.value}\n"
                        )

    def Set_Sprite(self):
        self.effect = self.type.replace('_potion', '')
        self.Update_Sub_Type()
        
        super().Set_Sprite()

    def Increase_Strength(self):
        self.strength += 1
    
    def Update_Sub_Type(self):
        if self.amount <= 1:
            self.sub_type = self.type + '_low'
        elif self.amount == 2:
            self.sub_type = self.type + '_half'
        elif self.amount >= 3:
            self.sub_type = self.type + '_full'


    def Activate(self):
        if not super().Activate():
            return
        if self.game.player.Set_Effect(self.effect, self.strength):
            self.Decrease_Amount(1)
            self.Set_Sprite()
            self.Set_Description()
        if self.amount <= 0:
            self.used = True
