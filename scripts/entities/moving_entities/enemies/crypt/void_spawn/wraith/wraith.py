from scripts.entities.moving_entities.enemies.crypt.void_spawn.void_spawn import Void_Spawn
from scripts.entities.moving_entities.enemies.crypt.void_spawn.wraith.wraith_effect import Wraith_Status_Effect_Handler
from scripts.engine.keys.keys import keys


class Wraith(Void_Spawn):

    _effect_handler = Wraith_Status_Effect_Handler

    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.wraith, health, strength, max_speed, agility, intelligence, stamina, 1, 15)
        self.active_weapon.Set_Damage(keys.slash, 5)
        self.Set_Effect(keys.soul_stealer, 5, True)
