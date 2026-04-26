from scripts.entities.moving_entities.enemies.behavior.abilities.shooting_functions.Shoot_Soul_Reaper import Shoot_Soul_Reaper
from scripts.entities.moving_entities.enemies.behavior.intent_manager import Intent_Manager
from scripts.entities.moving_entities.enemies.behavior.abilities.Dash import Dash

class Vampire_Intent_Manager(Intent_Manager):
    def __init__(self, game, entity):
        super().__init__(game, entity)
        self.dash = Dash(game, entity)
        self.actions['dash'] = self.Handle_Dash
        self.base_cooldown['dash'] = 0
        self.shoot_soul_reaper = Shoot_Soul_Reaper(self.game)

        self.actions['shoot_soul_reaper'] = self.Handle_Shoot_Soul_Reaper
        self.base_cooldown['shoot_soul_reaper'] = 10


    def Handle_Dash(self):
        if not self.dash.dashing:
            self.dash.Dash()

        self.dash.Dashing_Update()

        if self.dash.dashing == 1:
            self.Increment_Intent()
            self.entity.Set_Charge_To_Max()
        return

    def Handle_Shoot_Soul_Reaper(self):
        self.shoot_soul_reaper.Initialise_Shooting(self.entity)
        self.Increment_Intent()

        return