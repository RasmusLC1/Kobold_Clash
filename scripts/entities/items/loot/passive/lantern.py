from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys

class Lantern(Loot):
    def __init__(self, game, pos):
        super().__init__(game, keys.lantern, pos, (16, 16), 10, keys.passive)
        self.light_source = self.game.light_handler.Add_Light(self.pos, 9, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)


    def Pick_Up(self):
        if not super().Pick_Up():
            return False
        
        self.game.player.Update_Light_Source(9)
        self.game.light_handler.Remove_Light(self.light_source)
        return True
    
    def Place_Down(self):
        if not super().Place_Down():
            return False
        
        self.game.player.Update_Light_Source(self.game.player.default_light_level)
        self.game.light_handler.Add_Light_Source(self.light_source)
        self.light_source.Move_Light(self.pos, self.tile)
        return True
    
    def Update_Light_Level(self):
        return True
    
    def Update_Dark_Surface(self):
        self.rendered_image = self.entity_image