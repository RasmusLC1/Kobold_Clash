# Global registry dictionary
DECORATION_REGISTRY = {}

def register_ability(key):
    def decorator(cls): # cls = Classmethods
        DECORATION_REGISTRY[key] = cls
        return cls
    
    return decorator



from scripts.entities.decoration.ancient_tomb.shrine.blood_shrine import Blood_Shrine
from scripts.entities.decoration.shared.shrine.sacrifice_shrine import Sacrifice_Shrine
from scripts.entities.decoration.ancient_tomb.shrine.rune_shrine import Rune_Shrine
from scripts.entities.decoration.ancient_tomb.loot_container.bookshelf import Bookshelf
from scripts.entities.decoration.ancient_tomb.loot_container.effigy_tomb import Effigy_Tomb
