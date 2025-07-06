from scripts.entities.moving_entities.enemies.void_spawn.void_spawn import Void_Spawn
from scripts.engine.assets.keys import keys

class Phantom(Void_Spawn):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.phantom, health, strength, max_speed, agility, intelligence, stamina, 30, 20)
        self.active_weapon.Set_Damage(keys.slash, 6)
        
