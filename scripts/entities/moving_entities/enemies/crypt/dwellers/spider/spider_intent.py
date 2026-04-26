from scripts.entities.moving_entities.enemies.behavior.intent_manager import Intent_Manager
from scripts.entities.moving_entities.enemies.behavior.special_attacks.shooting_functions.Shoot_Spiderweb import Shoot_Spiderweb
from scripts.entities.moving_entities.enemies.behavior.special_attacks.Jump_Attack import Jump_Attack
from scripts.engine.keys.keys import keys

class Spider_Intent_Manager(Intent_Manager):
    def __init__(self, game, entity, attack_speed, path_finding_strategy, behavior):
        super().__init__(self, game, entity, attack_speed, path_finding_strategy, behavior)
        self.shoot_spiderweb = Shoot_Spiderweb(self.game)
        self.jump_attack = Jump_Attack(game, entity)
        self.actions['shoot_spiderweb'] = self.Shoot_Spiderweb
        self.base_cooldown['shoot_spiderweb'] = 10

        self.actions['jump_attack'] = self.Jump_Attack
        self.base_cooldown['jump_attack'] = 80
        self.base_cooldown[keys.keep_position] = 80


    def Shoot_Spiderweb(self):
        self.shoot_spiderweb.Initialise_Shooting(self.entity)
        self.Increment_Intent()

        return
    
    def Jump_Attack(self):
        self.jump_attack.Set_Attack_Length(30)
        if self.jump_attack.Jump_Attack(self.entity):
            self.Increment_Intent()
        return
    


