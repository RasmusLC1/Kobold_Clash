from scripts.entities.moving_entities.enemies.crypt.dwellers.dweller import Dweller
from scripts.engine.keys.keys import keys


# TODO: Implement intent with spider and make attacks into objects
class Spider(Dweller):

    def __init__(self, game, pos):
        super().__init__(game, pos, keys.spider)

        self.active_weapon.Set_Damage(keys.poison, 5)


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
        self.animation_handler.Set_Animation(keys.idle)



    def Update_Jumping_Animation(self) -> None:
        if not self.jumping_animation_num_cooldown:
            self.jumping_animation_num += 1
            if self.jumping_animation_num > self.jumping_animation_num_max:
                self.jumping_animation_num = 0
            self.jumping_animation_num_cooldown = self.jumping_animation_num_cooldown_max
        else:
            self.jumping_animation_num_cooldown = max(0, self.jumping_animation_num_cooldown - 1)

