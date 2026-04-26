from scripts.entities.items.weapons.magic_attacks.vampiric.soul_reap_shooter import Soul_Reap_Shooter
from scripts.entities.moving_entities.enemies.behavior.special_attacks.shooting_functions.shooting_function import Shooting_Function

class Shoot_Soul_Reaper(Shooting_Function):
    def __init__(self, game):
        super().__init__(game)
        self.soul_reaper = Soul_Reap_Shooter(game)

    def Initialise_Shooting(self, entity):
        entity.Set_Target(self.game.player.pos)
        entity.charge = 1
        entity.Attack_Direction_Handler()
        self.soul_reaper.Spawn_Soul_Reap(entity, 15)
