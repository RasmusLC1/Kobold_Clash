from scripts.entities.decoration.shared.shrine.shrine import Cycling_Shrine
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.ancient_tomb.ancient_tomb_registry import Register_Decoration


@Register_Decoration(keys.blood_shrine)
class Blood_Shrine(Cycling_Shrine):
    def __init__(self, game, pos, size=(64, 64)) -> None:
        super().__init__(game, keys.blood_shrine, pos, size, cooldown_range=(0.6, 0.8))
        self.description = "sacrifice blood\nfor power"
        self.max_animation = 3
        self.tile.Set_Physics(True)
        self.is_open = False

    def Open(self, generate_clatter=True):
        if self.empty:
            return False
        player = self.game.player
        player.Set_Health(player.health // 2)
        player.Set_Effect(keys.vampiric, 1, True)
        self.empty = True
        return True  # was `return False` — fixed