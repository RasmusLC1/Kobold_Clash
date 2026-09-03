from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration
import pygame

@Register_Decoration(keys.harmonic_crystal)
class Harmonic_Crystal(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.harmonic_crystal, pos, (32, 32),
                         max_animation=4, animation_cooldown_max=1.5)
        self.description = "Harmonic vibrations eminate\n from this crystal"

    def Update(self, delta_time):
        self.Check_Player_Distance()
        return super().Update(delta_time)

    def Open(self, generate_clatter=False):
        if self.empty:
            return False
        self.game.player.Increase_Souls(100)
        self.Generate_Sound(keys.harmonic_crystal, 0.5, 1000)
        self.empty = True
        return True
