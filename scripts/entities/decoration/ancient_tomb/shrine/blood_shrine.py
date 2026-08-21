from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.ancient_tomb.ancient_tomb_registry import Register_Decoration
import random

@Register_Decoration(keys.blood_shrine)
class Blood_Shrine(Decoration):
    def __init__(self, game, pos, size = (64, 64)) -> None:
        super().__init__(game, keys.blood_shrine, pos, size, False)
        self.description = "sacrifice blood\nfor power"
        self.animation_cooldown = 0
        self.max_animation = 3
        self.tile.Set_Physics(True)
        self.is_open = False

    
    def Update(self, delta_time):
        self.Update_Animation(delta_time)
        return super().Update(delta_time)

    def Open(self, generate_clatter = True):
        if self.empty:
            return False
        player = self.game.player

        player.Set_Health(player.health // 2)

        player.Set_Effect(keys.vampiric, 1, True)

        self.empty = True
        return False

    def animation_cooldown_Handler(self, delta_time):
        if self.animation_cooldown <= 0:
            self.animation_cooldown = random.uniform(0.6, 0.8)
            return True
        
        self.animation_cooldown -= delta_time
        return False



    def Update_Animation(self, delta_time):
        if not self.animation_cooldown_Handler(delta_time):
            return
        
        if self.animation >= self.max_animation:
            self.Set_Animation(0)
        else:
            self.Set_Animation(self.animation + 1)


