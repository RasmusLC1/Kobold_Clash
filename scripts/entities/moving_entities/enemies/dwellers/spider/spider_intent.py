from scripts.entities.moving_entities.enemies.behavior.intent_manager import Intent_Manager
from scripts.entities.moving_entities.enemies.attacks.Shoot_Spiderweb import Shoot_Spiderweb
from scripts.entities.moving_entities.enemies.attacks.Jump_Attack import Jump_Attack
from scripts.engine.assets.keys import keys

class Spider_Intent_Manager(Intent_Manager):
    def __init__(self, game, entity):
        super().__init__(game, entity)
        self.shoot_spiderweb = Shoot_Spiderweb(self.game)
        self.jump_attack = Jump_Attack()
        self.actions['shoot_spiderweb'] = self.Shoot_Spiderweb
        self.base_cooldown['shoot_spiderweb'] = 10

        self.actions['jump_attack'] = self.Jump_Attack
        self.base_cooldown['jump_attack'] = 80
        self.base_cooldown[keys.keep_position] = 80


    def Shoot_Spiderweb(self):
        self.shoot_spiderweb.Initialise_Spider_Web(self.entity)
        self.Increment_Intent()

        return
    
    def Jump_Attack(self):
        self.jump_attack.Set_Attack_Length(30)
        if self.jump_attack.Jump_Attack(self.entity):
            self.Increment_Intent()
        return
    


