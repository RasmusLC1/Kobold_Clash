from scripts.entities.decoration.shared.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys



class Chest(Loot_Container):
    def __init__(self, game, pos) -> None:
        self.version = 1
        super().__init__(game, keys.chest, pos, (32, 32), True, 20, keys.chest_break, 500)

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['version'] = self.version
        

    def Load_Data(self, data):
        super().Load_Data(data)
        self.version = data['version']

    def Open(self):
        if not super().Open():
            return False
        
        self.game.decoration_handler.Remove_Decoration(self)

        self.Generate_Sound(keys.chest_open, 0.1, 500)


    def Set_Loot_Types(self):
        self.loot_weights = {keys.passive : 0.05,
                             keys.key : 0.1,
                             keys.bomb : 0.2,
                             keys.potion : 0.3,
                             keys.revive : 0.05,
                             keys.utility : 0.2,
                             keys.curse : 0.1,
                             keys.valuable : 0.5}


