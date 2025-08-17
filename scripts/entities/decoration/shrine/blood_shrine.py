from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys


class Blood_Shrine(Decoration):
    def __init__(self, game, pos, size = (32, 32)) -> None:
        super().__init__(game, keys.blood_shrine, pos, size, False)
        self.tile.Set_Physics(True)
        self.is_open = False

    def Open(self, generate_clatter = True):
        if self.empty:
            return False
        player = self.game.player

        player.Set_Health(player.health // 2)

        player.Set_Effect(keys.vampiric, 1, True)

        self.empty = True
        return False


