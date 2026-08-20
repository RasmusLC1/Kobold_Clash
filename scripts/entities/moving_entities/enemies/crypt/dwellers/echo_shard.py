from scripts.entities.moving_entities.enemies.crypt.dwellers.dweller import Dweller
from scripts.engine.keys.keys import keys

class Echo_Shard(Dweller):

    def __init__(self, game, pos,):
        super().__init__(game, pos, keys.echo_shard)
        self.active_weapon.Set_Damage(keys.blunt, 5)
        self.Set_Ability(keys.echo_shard)