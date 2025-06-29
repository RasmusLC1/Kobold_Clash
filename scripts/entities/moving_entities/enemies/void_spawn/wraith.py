from scripts.entities.moving_entities.enemies.void_spawn.void_spawn import Void_Spawn
from scripts.entities.moving_entities.enemies.void_spawn.wraith_effect import Wraith_Status_Effect_Handler
from scripts.engine.assets.keys import keys


class Wraith(Void_Spawn):

    _effect_handler = Wraith_Status_Effect_Handler

    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.wraith, health, strength, max_speed, agility, intelligence, stamina, 60)
        self.active_weapon.Set_Damage(keys.slash, 5)
        self.Set_Effect(keys.soul_stealer, 5, True)


