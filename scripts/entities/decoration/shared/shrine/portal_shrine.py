from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.shared_registry import register_ability

@register_ability(keys.portal_shrine)
class Portal_Shrine(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.portal_shrine, pos, (64, 64))
        self.is_open = False
        self.animation = 0
        self.animation_cooldown = 0
        self.max_animation = 0
        self.min_animation = 0
        
        self.available_rune = None
        


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['is_open'] = self.is_open


    def Load_Data(self, data):
        super().Load_Data(data)
        self.is_open = data['is_open']

    def Update(self, delta_time):
        self.Update_Animation(delta_time)
        return super().Update(delta_time)

    def Update_Animation(self, delta_time):
        # Don't Set_Animation unless open
        if not self.is_open:
            return
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
        else:
            self.animation_cooldown = 0.3
            self.Set_Animation(random.randint(self.min_animation,self.max_animation))

    def Remove_Available_Rune(self):
        self.available_rune = None

    def Open(self):
        if not self.is_open:
            self.game.menu_handler.portal_shrine_menu.Initialise_Shrine(self)
            self.game.clatter.Generate_Clatter(self.pos, 400) # Generate clatter to alert nearby enemies
        self.game.player.Set_Last_Shrine(self)
        self.game.state_machine.Set_State('portal_shrine_menu')

    def Activate(self):
        self.light_level = 5
        self.light_source = self.game.light_handler.Add_Light(self.pos, self.light_level, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)
        self.max_animation = 3
        self.min_animation = 1
        self.is_open = True