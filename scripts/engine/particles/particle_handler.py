from scripts.engine.particles.particle import Particle
from scripts.engine.particles.particle_patterns import Particle_Patterns
from scripts.engine.keys.keys import keys
import random

class Particle_Handler:
    def __init__(self, game) -> None:
         self.game = game
         self.particle_pool = []
         self.active_particles = []
         self.index = 0
         self.Spawn_Particles(2000)

         self.particle_movement_patterns = {
             keys.dash_particle : Particle_Patterns.Dash_Particle,
             keys.fire_particle : Particle_Patterns.Fire_Particle,
             keys.electric_particle : Particle_Patterns.Spark_Particle,
             keys.blood_particle : Particle_Patterns.Spark_Particle,
             keys.gold_particle : Particle_Patterns.Spark_Particle,
             keys.loot_particle : Particle_Patterns.Spark_Particle,
             keys.bone_particle : Particle_Patterns.Spark_Particle,
             keys.soul_particle : Particle_Patterns.Soul_Particle,
             keys.vampire_particle : Particle_Patterns.Vampire_Particle,
             keys.strength_particle : Particle_Patterns.Vampire_Particle,
             keys.player_particle : Particle_Patterns.Player_Particle,
         }
         

    # Update the particles
    def Particle_Update(self, delta_time):
        for particle in self.active_particles:
                particle.Update(delta_time)

    def Particle_Render(self, surf, offset = (0,0)):
        for particle in self.active_particles:
                particle.Render(surf, offset)

    def Disable_Particle(self, particle):
        self.active_particles.remove(particle)


    def Activate_Particles(self, amount, type, pos, time = random.uniform(1, 1.5)):
        for _ in range(amount):
            particle = self.Find_Particle()

            # If none are found, spawn 100 new ones and attach one
            if not particle:
                particle = self.Spawn_Extra_Particle()

            # Get particle movement pattern
            velocity_function = self.particle_movement_patterns.get(type)
            velocity = velocity_function()

            # Activate particle and add to active particles
            particle.Set_Active(type, pos, velocity, time)
            particle.Set_Image(self.game.assets[type][particle.animation])
            self.active_particles.append(particle)


    # Search for particles with an index
    def Find_Particle(self):
        # If there are no particles in the pool return None to spawn particle
        if not self.particle_pool:
            return None
        
        # Check if the initial index is available, in which case loop the index back to 0
        if not self.particle_pool[0].lifespan:
            self.index = 0
        
        # Overflow prevent
        if self.index >= len(self.particle_pool) - 1:
            return None

        # Set the fire particle to be the next available index
        particle = self.particle_pool[self.index]
        self.index += 1

        # If there are no free fire particle return None to spawn a new one
        if particle.lifespan:
            return None
        
        return particle

    # Spawn single particle on demand
    def Spawn_Extra_Particle(self):
        particle = Particle(self)
        self.particle_pool.append(particle)
        return particle

    # Spawn bulk particles when initialised
    def Spawn_Particles(self, amount):
        for _ in range(amount):
             self.particle_pool.append(Particle(self))