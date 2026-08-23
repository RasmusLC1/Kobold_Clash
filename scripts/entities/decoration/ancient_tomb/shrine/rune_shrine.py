from scripts.entities.decoration.shared.shrine.shrine import Menu_Shrine
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.ancient_tomb.ancient_tomb_registry import Register_Decoration
from scripts.entities.decoration.shared.shrine.shrine_registry import Register_Shrine
import random

Register_Shrine(keys.rune_shrine)
@Register_Decoration(keys.rune_shrine)
class Rune_Shrine(Menu_Shrine):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.rune_shrine, pos, (64, 64), cycle_requires_open=False)
        self.max_animation = 3
        self.light_level = 8
        self.light_source = self.game.light_handler.Add_Light(self.pos, self.light_level, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)
        self.available_rune = None

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['rune_type'] = self.available_rune.type if self.available_rune else None

    def Load_Data(self, data):
        super().Load_Data(data)
        rune_type = data['rune_type']
        if rune_type:
            self.available_rune = self.game.item_handler.Spawn_Rune((999, 999), rune_type)

    def Remove_Available_Rune(self):
        self.available_rune = None

    def Open(self):
        if not self.is_open:
            self.Select_Available_Rune()
        if self.available_rune:
            self.game.menu_handler.rune_shrine_menu.Initialise_Runes(self, self.available_rune)
        else:
            self.game.menu_handler.rune_shrine_menu.Initialise_Runes(self)

        self.Activate_Shrine()
        self.game.state_machine.Set_State('rune_shrine_menu')
        self.game.clatter.Generate_Clatter(self.pos, 400)

    # TODO: NEEDS REWORK
    def Select_Available_Rune(self):
        rune_keys = list(self.game.rune_handler.runes.keys())
        random_key = random.choice(rune_keys)
        rune = self.game.rune_handler.runes[random_key]

        if rune in self.game.rune_handler.active_runes:
            self.Select_Available_Rune()
            return

        self.available_rune = rune
        self.is_open = True