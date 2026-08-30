
class UI():
    def __init__(self, game, pos_x, pos_y, max_animation, animation_cooldown_max):
        self.game = game
        self.animation = 0
        self.cooldown = 0
        self.max_animation = max_animation
        self.base_x = pos_x
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.animation_cooldown_max = animation_cooldown_max

    def Update(self, delta_time):
        self.Update_Animation(delta_time)

    def Update_Animation(self, delta_time, movement=(0, 0)):
        if not self.cooldown:
            if self.animation >= self.max_animation:
                self.animation = 0
            else:
                self.animation += 1
            self.cooldown = self.animation_cooldown_max

        self.cooldown -= delta_time
