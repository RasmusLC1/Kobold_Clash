from scripts.engine.keys.decorations import Decorations
from ..decoration_config import Decoration_Config

ANCIENT_TOMB_CONFIG = {
    Decorations.effigy_tomb: Decoration_Config(
            amount= (5, 10),
            size = (64, 64)
    ),

    Decorations.sacrifice_shrine: Decoration_Config(
            amount= (2, 3),
            size = (64, 64),
            check_player_path=True
    ),

    Decorations.blood_shrine: Decoration_Config(
            amount= (2, 3),
            size = (64, 64),
            check_player_path=True
    ),

}