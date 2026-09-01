from scripts.entities.decoration.shared.loot_container.plinth import Plinth
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration

@Register_Decoration(keys.plinth)
class Crystal_Plinth(Plinth):

    def Get_Loot_Types(self):
            self.loot_weights = {
                                 keys.gem : 1,
                                 }
    