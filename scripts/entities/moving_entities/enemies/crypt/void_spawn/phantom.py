from scripts.entities.moving_entities.enemies.crypt.void_spawn.void_spawn import Void_Spawn
from scripts.engine.keys.keys import keys

class Phantom(Void_Spawn):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.phantom)
        self.active_weapon.Set_Damage(keys.slash, 6)
        
