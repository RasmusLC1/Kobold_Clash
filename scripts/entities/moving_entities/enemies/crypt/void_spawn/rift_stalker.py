from scripts.entities.moving_entities.enemies.crypt.void_spawn.void_spawn import Void_Spawn
from scripts.engine.keys.keys import keys

class Rift_Stalker(Void_Spawn):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.rift_stalker)
        self.active_weapon.Set_Damage(keys.slash, 4)
        self.Set_Ability(keys.echo_teleport)
