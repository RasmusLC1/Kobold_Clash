from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.fire_spirit import Fire_Spirit
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.ice_spirit import Ice_Spirit
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.earth_elemental import Earth_Elemental
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.electric_elemental import Electric_Elemental
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.poison_elemental import Poison_Elemental
from scripts.entities.moving_entities.enemies.crystal_caverns.mythicals.medusa.medusa import Medusa
from scripts.entities.moving_entities.enemies.crystal_caverns.mythicals.minotaur import Minotaur
from scripts.entities.moving_entities.enemies.crypt.dwellers.spider.spider import Spider
from scripts.entities.moving_entities.enemies.enemy_spawner import Enemy_Spawner
from scripts.engine.keys.keys import keys

class Crystal_Cavern_Spawn(Enemy_Spawner):
    def __init__(self, game):
        spawn_methods = {
            keys.fire_spirit : Fire_Spirit,
            keys.ice_spirit: Ice_Spirit,
            keys.earth_elemental: Earth_Elemental,
            keys.electric_elemental: Electric_Elemental,
            keys.poison_elemental: Poison_Elemental,
            keys.minotaur: Minotaur,
            keys.medusa: Medusa,
            keys.spider: Spider,
        }

        enemy_types = {
            # keys.fire_spirit: 0.2,
            # keys.ice_spirit: 0.2,
            # keys.earth_elemental: 0.2,
            # keys.spider: 0.2,
            # keys.electric_elemental: 0.2,
            keys.poison_elemental: 0.2,
            # keys.minotaur: 0.2,
            # keys.medusa: 0.2,
        }
        super().__init__(game, spawn_methods, enemy_types)
    
 