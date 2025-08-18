from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys

class Brazier(Decoration):
    def __init__(self, game, pos) -> None:
        self.version = random.randint(1, 2)
        super().__init__(game, keys.brazier + '_' + str(self.version), pos, (32, 32))
        self.animation = 1
        self.max_animation = 5
        self.animation_cooldown = 0
        self.animation_cooldown_max = 0.8
        self.Add_Light()

    def Save_Data(self):
        self.type = keys.brazier # Set brazier to default version to make loading easier
        super().Save_Data()
        self.saved_data['version'] = self.version


    def Load_Data(self, data):
        super().Load_Data(data)
        self.version = data['version']
        self.type = keys.brazier + '_' + str(self.version)
        self.Set_Sprite()
    

    def Update(self, delta_time):
        if self.animation > 0: # animation 0 is off
            self.Update_Animation(delta_time)
        self.Update_Light_Level()
        
        return super().Update(delta_time)

    def Add_Light(self):
        self.light_source = self.game.light_handler.Add_Light(self.pos, 10, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)

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