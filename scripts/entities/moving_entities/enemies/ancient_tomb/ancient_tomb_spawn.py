 
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.skeleton_warrior import Skeleton_Warrior
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.skeleton_ranger import Skeleton_Ranger
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.skeleton_bell_toller import Skeleton_Bell_Toller
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.skeleton_cleric import Skeleton_Cleric
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.skeleton_undertaker import Skeleton_Undertaker 
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.skeleton_warlock import Skeleton_Warlock 
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.skeleton_guardian import Skeleton_Guardian 
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.skeleton_banner_bearer import Skeleton_Banner_Bearer 
from scripts.entities.moving_entities.enemies.ancient_tomb.dwellers.spider import Spider
from scripts.entities.moving_entities.enemies.ancient_tomb.dwellers.ghoul import Ghoul
from scripts.entities.moving_entities.enemies.ancient_tomb.dwellers.vampire import Vampire
from scripts.entities.moving_entities.enemies.ancient_tomb.void_spawn.shade import Shade
from scripts.entities.moving_entities.enemies.ancient_tomb.void_spawn.phantom import Phantom
from scripts.entities.moving_entities.enemies.ancient_tomb.void_spawn.wraith.wraith import Wraith
from scripts.entities.moving_entities.enemies.ancient_tomb.skeleton.wight_king import Wight_King
from scripts.entities.moving_entities.enemies.enemy_spawner import Enemy_Spawner
from scripts.engine.keys.keys import keys

class Crypt_Spawn(Enemy_Spawner):
    def __init__(self, game):
        spawn_methods = {
            keys.skeleton_warrior: Skeleton_Warrior,
            keys.skeleton_ranger : Skeleton_Ranger,
            keys.spider : Spider,
            keys.wight_king : Wight_King,
            keys.vampire : Vampire,
            keys.skeleton_bell_toller : Skeleton_Bell_Toller,
            keys.skeleton_cleric : Skeleton_Cleric,
            keys.skeleton_undertaker : Skeleton_Undertaker,
            keys.skeleton_warlock : Skeleton_Warlock,
            keys.skeleton_guardian : Skeleton_Guardian,
            keys.skeleton_banner_bearer : Skeleton_Banner_Bearer,
            keys.shade : Shade,
            keys.phantom : Phantom,
            keys.wraith : Wraith,
            keys.ghoul : Ghoul,
        }

        enemy_types = {
            keys.skeleton_warrior: 0.4,
            keys.skeleton_ranger: 0.2,
            keys.skeleton_bell_toller: 0.1,
            keys.skeleton_cleric: 0.05,
            keys.skeleton_undertaker: 0.05,
            keys.skeleton_guardian: 0.2,
            keys.skeleton_warlock: 0.05,
            keys.skeleton_banner_bearer: 0.05,
            keys.phantom: 0.1,
            keys.wraith: 0.05,
            keys.shade: 0.05,
            keys.spider: 0.1,
            keys.ghoul: 0.2,
            keys.wight_king: 0.01,
            keys.vampire: 0.01,
        }
        super().__init__(game, spawn_methods, enemy_types)
        