from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys


class Fragile_Wall(Decoration):
    def __init__(self, game, pos, size = (32, 32)) -> None:
        super().__init__(game, keys.fragile_wall, pos, size, True, 100, 'wall_break', 1000)
        if not self.tile:
            self.Delete()
            return
        self.tile.Set_Physics(True)
        self.tile.Set_Translucent(False)

       # TODO: IMPLEMENT walls that can be walked through, I.E walls without physics in tilemap
    def Open(self, generate_clatter = True):
        self.tile.Set_Physics(False)
        self.tile.Set_Translucent(True)

        self.render = False
        self.game.decoration_handler.Remove_Decoration(self)


    # Open the wall if it is destroyed
    def Destroyed(self):
        destroyed = super().Destroyed()

        if not destroyed:
            return False
        
        self.Open()
        return True
        
