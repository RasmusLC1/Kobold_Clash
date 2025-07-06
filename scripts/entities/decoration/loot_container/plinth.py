from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
import random

class Plinth(Decoration):
    def __init__(self, game, pos):
        super().__init__(game, keys.plinth, pos, (32, 32), True, 20)
        
        

    def Spawn_Rune(self):
        runes = {
            keys.dash_rune : 0.2,
            keys.healing_rune : 0.2,
            keys.speed_rune : 0.2,
            keys.increase_strength_rune : 0.2,
            keys.vampiric_rune : 0.2,

            keys.arcane_hunger_rune : 0.2,
            keys.light_rune : 0.4,
            keys.magnet_rune : 0.2,

            keys.fire_resistance_rune : 0.2,
            keys.fire_spray_rune : 0.1,
            keys.freeze_spray_rune : 0.1,
            keys.poison_resistance_rune : 0.2,
            keys.electric_spray_rune : 0.1,

        }
        rune_type = random.choices(
                    population=list(runes.keys()),
                    weights=list(runes.values()),
                    k=1
                )[0]
        self.game.rune_handler.Spawn_Rune_Floor(rune_type, (self.pos[0] + 3, self.pos[1]))

