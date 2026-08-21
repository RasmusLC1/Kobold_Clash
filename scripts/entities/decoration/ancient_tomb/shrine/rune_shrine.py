from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.ancient_tomb.ancient_tomb_registry import Register_Decoration
import random

@Register_Decoration(keys.rune_shrine)
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

    # TODO: Might need a rework for the available rune
    def Load_Data(self, data):
        super().Load_Data(data)
        self.is_open = data['is_open']
        rune_type = data['rune_type']
        if not rune_type:
            return
        self.available_rune = self.game.item_handler.Spawn_Rune((999,999), rune_type)



    def Update(self, delta_time):
        self.Update_Animation(delta_time)
        return super().Update(delta_time)

    def Update_Animation(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
        else:
            self.animation_cooldown = 0.3
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
        
    # TODO: NEEDS REWORK
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
