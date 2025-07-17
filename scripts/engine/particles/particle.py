import random
from scripts.engine.keys.keys import keys


class Particle:
    def __init__(self, particle_handler):
        self.particle_handler = particle_handler
        self.type = None # Dictates it's movement and texture
        self.pos = (-999, -999) # Position is set off screen and moved to correct location on demand
        self.velocity = (0, 0) # Handles the movement pattern
        self.image = None # Set the image when particle is activated
        self.lifespan = 0 # How long a particle is active
        self.initial_lifespan = 0 # Holder for lifespan
        self.animation = 0 # Sparks always have 6 variations

    def Set_Type(self, type):
        self.type = type
        self.animation = random.randint(0, 5)

    def Set_Image(self, image):
        self.image = image

    def Set_Lifespan(self, lifespan_seconds):
        self.lifespan = lifespan_seconds
        self.initial_lifespan = lifespan_seconds

    def Set_Position(self, pos):
        self.pos = pos

    def Set_Velocity(self, velocity):
        self.velocity = velocity

    # Activate the particle by setting attributes
    def Set_Active(self, type, pos, velocity, frame):
        self.Set_Type(type)
        self.Set_Lifespan(frame)
        self.Set_Position(pos)
        self.Set_Velocity(velocity)
    
    # Disable the particle, by setting all the attributes back to default
    def Disable(self):
        self.image = None
        self.lifespan = 0
        self.Set_Position((-999, -999))
        self.Set_Velocity((0,0))
        self.particle_handler.Disable_Particle(self)

    def Update(self, delta_time):
        # If framecount = 0 then the particle is not active and therefore does not need to be updated
        if not self.lifespan:
            return True
        self.pos = (
                    self.pos[0] + self.velocity[0] * delta_time,
                    self.pos[1] + self.velocity[1] * delta_time
                    )

        self.Update_Lifespan(delta_time)        
    
    # If framecount is zero, return true to signal the particle is finished and no longer active
    def Update_Lifespan(self, delta_time):
        self.lifespan -= delta_time
        if self.lifespan <= 0:
            self.Disable()
            return True
        return False


    def Render(self, surf, offset=(0, 0)):
        if not self.lifespan:
            return
        image = self.image.copy()
        alpha = int(255 * (self.lifespan / self.initial_lifespan))
        image.set_alpha(alpha)
        surf.blit(image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    