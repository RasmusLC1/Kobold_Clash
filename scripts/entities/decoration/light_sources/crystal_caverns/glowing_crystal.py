from scripts.entities.decoration.light_sources.light_sources.light_source import Light_Source
import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.light_sources.crystal_caverns.light_sources_registry import Register_Light_Source


@Register_Light_Source(keys.glowing_crystal, 0.5)
class Glowing_Crystal(Light_Source):
    def __init__(self, game, pos) -> None:
        version = random.randint(1, 5)
        super().__init__(game, pos, keys.glowing_crystal, version, strength=8, max_animation=5, animation_cooldown_max=0.9)
    

    def Update(self, delta_time):
        if self.animation > 0: # animation 0 is off
            self.Update_Animation(delta_time)
        self.Update_Light_Level()
        
        return super().Update(delta_time)

    def Damage_Taken(self, damage, effect):
        self.game.clatter.Generate_Clatter(self.pos, damage * 10)

        
    def Update_Animation(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
        else:
            self.Animate()

    def Animate(self):
        self.animation_cooldown = random.uniform(self.animation_cooldown_max - 0.2, self.animation_cooldown_max)
        self.Set_Animation(random.randint(1,self.max_animation))
