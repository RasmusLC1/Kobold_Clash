from scripts.entities.moving_entities.enemies.void_spawn.void_spawn import Void_Spawn
from scripts.engine.assets.keys import keys

class Shade(Void_Spawn):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.shade, health, strength, max_speed, agility, intelligence, stamina, 60)
        self.active_weapon.Set_Damage(keys.slash, 4)


    
    def Set_Target(self, pos):
        self.target = self.game.player.pos