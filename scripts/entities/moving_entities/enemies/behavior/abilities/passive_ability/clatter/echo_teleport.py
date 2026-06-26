from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
import random

class Echo_Teleport(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)

    # Always registrer noises and path towards them
    def Update(self, delta_time):
        super().Update(delta_time)
        if self.entity.locked_on_target:
            return
        
        clatter_pos = self.game.clatter.Check_If_Noise_Generated()
        
        # Only act on the precise frame the noise is created
        if clatter_pos:
            pos_x = clatter_pos[0] + random.randint(-100, 100)
            pos_y = clatter_pos[1] + random.randint(-100, 100)
            self.entity.Set_Position((pos_x, pos_y))
