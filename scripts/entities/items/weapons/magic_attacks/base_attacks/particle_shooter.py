from scripts.engine.keys.keys import keys


class Particle_Shooter():
    def __init__(self, game):
        self.game = game
        self.index = 0
        self.particle_pool = []
        self.base_damage = 0
        self.cooldown = 0
        self.charge = 0
        self.entity = None
        self.ready_to_shoot = False

    def Update(self, delta_time):
        if not self.charge:
            return
        
        if not self.Handle_Cooldown(delta_time):
            return False
        
        self.Generate_Projectile()

    def Generate_Projectile(self):
        self.Particle_Creation(self.entity, 3, cooldown=0.5)
        self.ready_to_shoot = False
        self.charge -= 1
        return
    
    def Handle_Cooldown(self, delta_time):
        if not self.charge:
            return False
        
        if self.cooldown <= 0:
            return True
        self.cooldown -= delta_time
        return False
    
    def Check_Shooting_Ready(self, delta_time):
        if not self.charge:
            return
        
        self.ready_to_shoot = self.flame_thrower.Update(delta_time)
        if not self.ready_to_shoot:
            return
        
        self.Generate_Projectile()

    def Initialise_Shooting(self, entity, charge, damage):
        self.entity = entity
        self.charge = charge
        self.base_damage = damage
        self.ready_to_shoot = True

    def Particle_Creation(self, special_attack):
        pass
            
    def Shoot_Particles(self, special_attack):
        pass
    
    # Append extra fire particle to the pool in case it runs out
    def Create_Extra_Particle(self):
        pass
    
    # Effect is ignored as this is a general weapons function
    def Set_Damage(self, effect, amount):
        self.base_damage += amount

    # Search for particles with an index
    def Find_Particle(self):
        # If there are no particles in the pool return None to spawn particle
        if not self.particle_pool:
            return None
        
        # Check if the initial index is available, in which case loop the index back to 0
        if not self.particle_pool[0].delete_countdown:
            self.index = 0
        
        # Overflow prevent
        if self.index >= len(self.particle_pool) - 1:
            return None

        # Set the fire particle to be the next available index
        particle = self.particle_pool[self.index]
        self.index += 1

        # If there are no free fire particle return None to spawn a new one
        if particle.delete_countdown:
            return None
        
        return particle
