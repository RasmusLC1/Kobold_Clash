from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys


class Light_Source(Decoration):
    def __init__(self, game, pos, type, version, light_strength, destructable=False, health=0,
                         destruction_sound=None, destruction_clatter = 500, animation=1, 
                         max_animation = 0, animation_cooldown_max = 0) -> None:
        self.version = version
        super().__init__(game, type + '_' + str(version), pos, (32, 32),
                         destructable=destructable, health=health,
                         destruction_sound=destruction_sound,
                         destruction_clatter=destruction_clatter, animation=animation,
                         max_animation=max_animation,
                         animation_cooldown_max=animation_cooldown_max)
        
        self.light_strength = light_strength
        self.Add_Light()

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['version'] = self.version
        self.saved_data['type'] = self.type


    def Load_Data(self, data):
        super().Load_Data(data)
        self.version = data['version']
        self.type = data['type']
        self.Set_Sprite()
    
    def Add_Light(self):
        self.light_source = self.game.light_handler.Add_Light(self.pos, self.light_strength, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)

