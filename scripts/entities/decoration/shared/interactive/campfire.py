from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.shared_registry import Register_Decoration
from scripts.entities.entity.fire_animation_handler import Fire_Animation_Handler

@Register_Decoration(keys.campfire)
class Campfire(Decoration):
    _animation_handler = Fire_Animation_Handler

    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.campfire, pos, (32, 32), max_animation=4, animation_cooldown_max=0.8)
        self.description = "Light a fire\nRest and recover"


    def Open(self, generate_clatter=False):
        if self.empty:
            return False
        self.Add_Light()
        player = self.game.player
        self.empty = True
        
        player.Set_Effect(keys.healing, player.max_health // 2) # Heal player for half health
        self.game.clatter.Increase_Awakening() # Increase awakening when lighting fire
        self.Set_Animation(1)
        return True
            
    
    def Add_Light(self):
        self.light_source = self.game.light_handler.Add_Light(self.pos, 10, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)

    def Update_Animation(self, delta_time, movement=(0, 0)):
        if not super().Update_Animation(delta_time, movement):
            return False
        self.Spawn_Fire_Particle()
        return True

    def Spawn_Fire_Particle(self):
        self.game.particle_handler.Activate_Particles(random.randint(1, 2), keys.fire_particle, self.rect().center)
        return