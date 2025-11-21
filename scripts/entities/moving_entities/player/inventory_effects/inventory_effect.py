from scripts.engine.keys.keys import keys

class Inventory_Effect():

    def __init__(self, entity, effect):
        self.player = entity
        self.effect = effect
        self.description = ''
        self.Set_Decription()
        
    def Update(self):
        pass

    def Enable(self, effect_strength = 1):
        self.player.Set_Effect(self.effect, effect_strength, True)
        

    def Disable(self, effect_strength = 1):
        self.player.Remove_Effect(self.effect, effect_strength)
    def Damage_Taken(self):
        pass

    def Set_Decription(self):
        pass