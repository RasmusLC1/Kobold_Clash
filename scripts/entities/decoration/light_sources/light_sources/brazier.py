from scripts.entities.decoration.light_sources.light_sources.light_source import Light_Source
import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.light_sources.ancient_tomb.light_sources_registry import Register_Light_Source
from scripts.entities.entity.fire_animation_handler import Fire_Animation_Handler

@Register_Light_Source(keys.brazier, 0.4)
class Brazier(Light_Source):

    _animation_handler = Fire_Animation_Handler 

    def __init__(self, game, pos) -> None:
        version = random.randint(1, 2)
        max_animation = 5
        start_animation = random.randint(1, max_animation)
        super().__init__(game, pos, keys.brazier, version, light_strength=10,
                         animation=start_animation, max_animation=max_animation,
                         animation_cooldown_max=0.8)
    

    def Update(self, delta_time):
        self.Update_Light_Level()
        
        return super().Update(delta_time)

    # Turn off the fire
    def Open(self, generate_clatter=False):
        if self.animation > 0:
            self.animation_handler.Set_Frame(0)
            self.game.light_handler.Remove_Light(self.light_source)
            self.light_source = None
        else:
            if self.light_source:
                print("BRAZIER Lightsource error", vars(self))
                return False
            self.Add_Light()
            self.animation_handler.Set_Random_Animation()
            self.Spawn_Fire_Particle()
            
        return True

        
    def Update_Animation(self, delta_time):
        if not super().Update_Animation(delta_time):
            return False
        self.Spawn_Fire_Particle()
        return True

    def Spawn_Fire_Particle(self):
        self.game.particle_handler.Activate_Particles(random.randint(1, 2), keys.fire_particle, self.rect().center)
        return