from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration


@Register_Decoration(keys.harmonic_crystal)
class Harmonic_Crystal(Decoration):
    SOUL_REWARD = 100
    SOUND_VOLUME = 0.5
    SOUND_RANGE = 1000

    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.harmonic_crystal, pos, (32, 32),
                         max_animation=4, animation_cooldown_max=1.5)
        self.description = "Harmonic vibrations emanate\nfrom this crystal"
        self.empty = False

    def Open(self, generate_clatter=False) -> bool:
        """Grant souls to the player once; later calls do nothing."""
        if self.empty:
            return False

        self.empty = True
        self.game.player.Increase_Souls(self.SOUL_REWARD)
        self.Generate_Sound(keys.harmonic_crystal, self.SOUND_VOLUME, self.SOUND_RANGE)
        return True