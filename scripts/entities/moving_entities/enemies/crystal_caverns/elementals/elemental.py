from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.engine.keys.keys import keys


class Elemental(Enemy):
    def __init__(self, game, pos, type, touching_ground = False):
        super().__init__(game, pos, type)
        self.touching_ground = touching_ground
        self.Set_Ability(keys.crystal_scale)