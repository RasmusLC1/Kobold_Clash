from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.shared_registry import register_ability


@register_ability(keys.door_basic)
class Door(Decoration):
    def __init__(self, game, pos, size = (32, 32)) -> None:
        super().__init__(game, keys.door_basic, pos, size, True, 50, 'door_destroyed', 700)
        self.is_open = False
        self.high_light_cooldown = 0
        if not self.tile:
            self.Delete()
            return
        self.tile.Set_Physics(True)

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['is_open'] = self.is_open


    def Load_Data(self, data):
        super().Load_Data(data)
        self.is_open = data['is_open']
        if self.is_open:
            self.Open(False)

    def Update(self, delta_time):
        if not self.high_light_cooldown:
            return
        self.high_light_cooldown -= delta_time


    def Set_Highlight(self):
        self.high_light_cooldown = 0.5


    # TODO: IMPLEMENT walls that can be walked through, I.E walls without physics in tilemap
    def Open(self, generate_clatter = True):
        self.is_open = True
        self.tile.Set_Physics(False)
        self.tile.Set_Translucent(True)

        self.render = False
        self.game.decoration_handler.Remove_Decoration(self)
        if generate_clatter:
            self.Generate_Sound(keys.door_open, 1, 700) # Generate clatter to alert nearby enemies


    def Destroyed(self):
        destroyed = super().Destroyed()

        if not destroyed:
            return False
        
        self.Open(False)
        return True
        

    def Render(self, surf, offset = (0,0)):
        super().Render(surf, offset)
        if not self.high_light_cooldown:
            return
        self.Lightup(self.rendered_image)

    def Update_Dark_Surface(self):
        if self.high_light_cooldown:
            return
        return super().Update_Dark_Surface()

