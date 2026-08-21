from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys


class Light_Source(Decoration):
    def __init__(self, game, pos, type, version, strength, max_animation = 0, animation_cooldown_max = 0) -> None:
        self.version = version
        super().__init__(game, type + '_' + str(version), pos, (32, 32))
        self.animation = 1
        self.max_animation = max_animation
        self.animation_cooldown = 0
        self.strength = strength
        self.animation_cooldown_max = animation_cooldown_max
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
        self.light_source = self.game.light_handler.Add_Light(self.pos, self.strength, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)

