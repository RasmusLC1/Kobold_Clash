from scripts.entities.decoration.light_sources.light_sources.light_source import Light_Source
import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.light_sources.ancient_tomb.light_sources_registry import Register_Light_Source


@Register_Light_Source(keys.brazier, 0.4)
class Brazier(Light_Source):
    def __init__(self, game, pos) -> None:
        version = random.randint(1, 2)
        super().__init__(game, pos, keys.brazier, version, strength=10, max_animation=5, animation_cooldown_max=0.8)
    

    def Update(self, delta_time):
        if self.animation > 0: # animation 0 is off
            self.Update_Animation(delta_time)
        self.Update_Light_Level()
        
        return super().Update(delta_time)

    # Turn off the fire
    def Open(self, generate_clatter=False):
        if self.animation > 0:
            self.Set_Animation(0)
            self.game.light_handler.Remove_Light(self.light_source)
            self.light_source = None
        else:
            if self.light_source:
                print("BRAZIER Lightsource error", vars(self))
                return False
            self.Add_Light()
            self.Animate()
            
        return True

        
    def Update_Animation(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
        else:
            self.Animate()

    def Animate(self):
        self.Spawn_Fire_Particle()

        self.animation_cooldown = random.uniform(self.animation_cooldown_max - 0.2, self.animation_cooldown_max)
        self.Set_Animation(random.randint(1,self.max_animation))


    def Spawn_Fire_Particle(self):
        self.game.particle_handler.Activate_Particles(random.randint(1, 2), keys.fire_particle, self.rect().center)
        return