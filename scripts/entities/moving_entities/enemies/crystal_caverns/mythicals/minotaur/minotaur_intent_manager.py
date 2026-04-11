from scripts.entities.moving_entities.enemies.behavior.intent_manager import Intent_Manager
from scripts.entities.moving_entities.enemies.attacks.Dash import Dash
from scripts.engine.keys.keys import keys

class Minotaur_Intent_Manager(Intent_Manager):
    def __init__(self, game, entity, attack_speed, path_finding_strategy, behavior, max_weapon_charge):
        super().__init__(game, entity, attack_speed, path_finding_strategy, behavior, max_weapon_charge)
        self.dash = Dash(game, entity)
        self.actions['dash'] = self.Handle_Dash
        self.base_cooldown['dash'] = 0


    def Handle_Dash(self):
        if not self.dash.dashing:
            self.dash.Dash()

        self.dash.Dashing_Update()

        if self.dash.dashing == 1:
            self.Increment_Intent()
            self.entity.Set_Charge_To_Max()
        return
