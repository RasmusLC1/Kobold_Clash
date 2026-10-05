from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration
import random

@Register_Decoration(keys.harmonic_crystal)
class Harmonic_Crystal(Decoration):
    SOUL_REWARD = 100
    SOUND_VOLUME = 0.5
    SOUND_RANGE = 1000

    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.harmonic_crystal, pos, (32, 32),
                         max_animation=3, animation_cooldown_max=1.5)
        self.description = "Harmonic vibrations emanate\nfrom this crystal"
        self.empty = False
        self.animation_handler.Set_Min_Animation(1)

    # Grant souls to the player once; later calls do nothing
    def Open(self, generate_clatter=False) -> bool:
        if self.empty:
            return False

        self.empty = True
        self.game.player.Increase_Souls(self.SOUL_REWARD)
        self.Generate_Sound(keys.harmonic_crystal, self.SOUND_VOLUME, self.SOUND_RANGE)
        pos_x = self.rect().x + self.size[0]
        pos_y = self.rect().y + self.size[1]
        self.game.particle_handler.Activate_Particles(
            random.randint(20, 30), keys.soul_particle, (pos_x, pos_y), time=2
        )
        self.animation_handler.Set_Static_Animation(0)
        return True