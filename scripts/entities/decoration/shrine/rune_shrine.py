from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys

class Rune_Shrine(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.rune_shrine, pos, (64, 64))
        self.is_open = False
        self.animation = 0
        self.animation_cooldown = 0
        self.max_animation = 3
        self.light_level = 8
        self.light_source = self.game.light_handler.Add_Light(self.pos, self.light_level, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)
        self.available_rune = None
        


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['is_open'] = self.is_open
        if not self.available_rune:
            self.saved_data['rune_type'] = None
            return
        
        self.saved_data['rune_type'] = self.available_rune.type
        print(self.is_open, self.available_rune.type)


    def Load_Data(self, data):
        super().Load_Data(data)
        self.is_open = data['is_open']
        rune_type = data['rune_type']
        if not rune_type:
            return
        self.available_rune = self.game.rune_handler.Get_Rune(rune_type)



    def Update(self):
        self.Update_Animation()
        return super().Update()

    def Update_Animation(self):
        if self.animation_cooldown:
            self.animation_cooldown -= 1
        else:
            self.animation_cooldown = 20
            self.Set_Animation(random.randint(0,self.max_animation))

    def Remove_Available_Rune(self):
        self.available_rune = None

    def Open(self):
        if not self.is_open:
            self.Select_Available_Rune()
        if self.available_rune:
            self.game.menu_handler.rune_shrine_menu.Initialise_Runes(self, self.available_rune)
        else:
            self.game.menu_handler.rune_shrine_menu.Initialise_Runes(self)
        
        self.game.player.Set_Last_Shrine(self)
        self.game.state_machine.Set_State('rune_shrine_menu')
        self.game.clatter.Generate_Clatter(self.pos, 400) # Generate clatter to alert nearby enemies
        

    def Select_Available_Rune(self):
        # Convert the dictionary keys into a list
        rune_keys = list(self.game.rune_handler.runes.keys())

        # Pick a random key from the dictionary
        random_key = random.choice(rune_keys)

        # Get the rune object using the random key
        rune = self.game.rune_handler.runes[random_key]

        # Check if the rune is already active
        if rune in self.game.rune_handler.active_runes:
            self.Select_Available_Rune()
            return
        
        self.available_rune = rune
        self.is_open = True
