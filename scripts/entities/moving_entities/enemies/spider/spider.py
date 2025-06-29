from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.moving_entities.enemies.attacks.Shoot_Spiderweb import Shoot_Spiderweb
from scripts.entities.moving_entities.enemies.spider.spider_intent import Spider_Intent_Manager
from scripts.engine.assets.keys import keys

# TODO: Implement intent with spider and make attacks into objects
class Spider(Enemy):

    intent_manager_class = Spider_Intent_Manager

    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, 60, 'dweller')

        self.animation = keys.spider + '_' + 'idle'

        self.path_finding_strategy = 'standard'
        self.intent_manager.Set_Intent(['medium_range', 'keep_position', 'shoot_spiderweb', 'direct', 'jump_attack', 'long_range'])

        self.animation_num_max = 3 # running and idle animation
        self.animation_num_cooldown_max = 100

        self.attack_animation_num_max = 3 # Standard attack and shoot spider web
        self.attack_animation_num_cooldown_max = 200

        self.jumping_animation_num_max = 8 # Jumping attack
        self.jumping_animation_num = 0
        self.jumping_animation_num_cooldown_max = 5

        self.on_back_animation_num_max = 8 # To make spider friendly again
        self.on_back_animation_num_cooldown_max = 50

        self.attack_cooldown = 0


        self.attack_symbol_offset = 10
    


    # Set new action for animation
    def Set_Action(self, movement = None):
        if not movement:
            return
        
        if self.intent_manager.jump_attack.attack_length:
            self.animation_handler.Set_Animation('jumping')
            return

        if self.charge and self.distance_to_player <= 50:
            self.animation_handler.Set_Animation(keys.attack)
            return

        
        if movement[1] or movement[0]:
            self.animation_handler.Set_Animation('running')
            return
        self.animation_handler.Set_Animation('idle')




    def Update(self, tilemap, movement = (0, 0)):
        super().Update(tilemap, movement)
        self.Update_Attack_Cooldown()

    
    # Bite the player when the player is close
    def Attack(self):
        if not super().Attack():
            return
        if self.distance_to_player < 40:
            self.game.player.Damage_Taken(self.strength)
            self.game.player.Set_Effect(keys.poison, 4)
            self.Set_Attack_Cooldown(60)
            return True
        


    def Update_Attack_Cooldown(self):
        if self.attack_cooldown:
            self.attack_cooldown = max(0, self.attack_cooldown - 1)
        return

    

    
    def Update_Jumping_Animation(self) -> None:
        if not self.jumping_animation_num_cooldown:
            self.jumping_animation_num += 1
            if self.jumping_animation_num > self.jumping_animation_num_max:
                self.jumping_animation_num = 0
            self.jumping_animation_num_cooldown = self.jumping_animation_num_cooldown_max
        else:
            self.jumping_animation_num_cooldown = max(0, self.jumping_animation_num_cooldown - 1)


    def Set_Attack_Cooldown(self, amount):
        self.attack_cooldown = amount
        return
