from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration

@Register_Decoration(keys.crystal_fountain)
class Crystal_Fountain(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.crystal_fountain, pos, (32, 32),
                         max_animation=4, animation_cooldown_max=1.3)
        self.description = "Crystal clear waters flow"
        self.effect_strength = 4

    def Open(self, generate_clatter=False):
        player = self.game.player
        # Prevents the player from adding effect if they already have resistance
        if player.Get_Effect(keys.resistance):
            return False

        player.Set_Effect(keys.resistance, self.effect_strength)
        self.Generate_Sound(keys.crystal_fountain, 0.4, 100)

        return True