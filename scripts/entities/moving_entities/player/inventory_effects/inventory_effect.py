from scripts.engine.keys.keys import keys

class Inventory_Effect():

    def __init__(self, entity, effect):
        self.player = entity
        self.effect = effect
        self.description = ''
        self.Set_Decription()
        
    def Update(self):
        pass

    def Enable(self):
        pass

    def Disable(self):
        pass

    def Damage_Taken(self):
        pass

    def Set_Decription(self):
        pass