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
        self.base_cooldown['jump_attack'] = 0
        self.base_cooldown['keep_position'] = 80
        self.base_cooldown['long_range'] = 80

        self.actions['long_range'] = self.Long_Range

    def Shoot_Spiderweb(self):
        self.shoot_spiderweb.Initialise_Spider_Web(self.entity)
        self.Increment_Intent()

        return
    
    def Jump_Attack(self):
        self.jump_attack.Set_Attack_Length(30)
        if self.jump_attack.Jump_Attack(self.entity):
            self.Increment_Intent()
        return
    
    def Long_Range(self):
        if self.entity.max_speed != self.entity.max_speed_holder:
                self.entity.max_speed = self.entity.max_speed_holder
        self.Set_Attack_Strategy("long_range")


    def Handle_Attack(self):
        pass

    def Update_Attack_Cooldown(self):
        if not super().Update_Attack_Cooldown():
            return False

        if self.entity.distance_to_player < self.entity.attack_distance:
            self.entity.Attack()
            
            return False

        if self.entity.charge:
            self.entity.charge = 0
            self.attack_cooldown = 0

        return True