from scripts.engine.keys.decorations import Decorations
from ...decoration.decoration_config import Decoration_Config

SHARED_DECRATION_CONFIG = {
    Decorations.chest: Decoration_Config(
        amount= (10, 20),
        size = (32, 32)
    ),

    Decorations.vase: Decoration_Config(
            amount= (15, 30),
            size = (32, 32)
    ),

    Decorations.weapon_rack: Decoration_Config(
            amount= (10, 20),
            size = (32, 32)
    ),

    Decorations.lever: Decoration_Config(
            amount= (4, 7),
            size = (32, 32)
    ),

    Decorations.campfire: Decoration_Config(
            amount= (1, 1),
            size = (32, 32)
    ),
    
    Decorations.teleportation_circle: Decoration_Config(
            amount= (10, 20),
            size = (32, 32)
    ),
    
    Decorations.hunter_shrine: Decoration_Config(
            amount= (3, 5),
            size = (64, 64)
    ),
    
    Decorations.hunter_shrine: Decoration_Config(
            amount= (3, 5),
            size = (64, 64)
    ),
    
    Decorations.portal_shrine: Decoration_Config(
            amount= (2, 3),
            size = (64, 64),
            check_player_path=True
    ),
    
    Decorations.soul_well: Decoration_Config(
            amount= (2, 3),
            size = (64, 64),
            check_player_path=True
    ),

}