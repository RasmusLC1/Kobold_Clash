from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys

class Campfire(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.campfire, pos, (32, 32))
        self.description = "Light a fire\nRest and recover"
        self.max_animation = 5
        self.animation_cooldown = 0
        self.animation_cooldown_max = 0.8


    def Open(self, generate_clatter=False):
        if not self.empty:
            self.Add_Light()
            player = self.game.player
            self.empty = True
            
            player.Set_Effect(keys.healing, player.max_health // 2) # Heal player for half health
            self.game.clatter.Increase_Awakening() # Increase awakening when lighting fire
            return True
            
        return False
    
    def Add_Light(self):
        self.light_source = self.game.light_handler.Add_Light(self.pos, 10, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)

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