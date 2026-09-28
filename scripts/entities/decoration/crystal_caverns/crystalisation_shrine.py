from scripts.entities.decoration.shared.shrine.shrine import Cycling_Shrine
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration
import pygame
from scripts.engine.utility.rect_handler import Rect_Handler


@Register_Decoration(keys.crystalisation_shrine)
class Crystalisation_Shrine(Cycling_Shrine):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.crystalisation_shrine, pos,
                         max_animation=4, animation_cooldown_max=1.5)
        self.description = "Trade gem for another"

