from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.engine.keys.keys import keys

CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX = 1 # heals 1 health every second

class Elemental(Enemy):
    def __init__(self, game, pos, type):
        super().__init__(game, pos, type)
        self.touching_ground = False
        self.Set_Ability(keys.crystal_scale)

