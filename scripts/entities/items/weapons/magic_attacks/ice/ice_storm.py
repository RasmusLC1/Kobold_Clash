from scripts.entities.items.weapons.magic_attacks.ice.ice_particle import Ice_Particle
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.entities.entities import PhysicsEntity
import math
import random
from scripts.engine.keys.keys import keys


class Ice_Storm(PhysicsEntity):
    def __init__(self, game, entity, duration):
        super().__init__(game, keys.ice_storm, keys.magic_attack, entity.pos, (32,32))
        self.entity = entity
        self.ice_cooldown = 0
        self.duration = 0
        self.animation = 0
        self.animation_max = 9
        self.ice_shooter = Ice_Shooter(game)
        self.Set_Duration(duration * 10)

    def Update(self):
        self.pos = (self.entity.pos[0], self.entity.pos[1] + 8)
        if self.Update_Cooldown():
            self.Ice_Particle_Creation()

    def Set_Duration(self, duration):
        self.duration += max(0, duration)

    def Reset_Duration(self):
        self.duration = 0

    def Update_Cooldown(self):
        if self.ice_cooldown:
            self.ice_cooldown -= 1
            return False
        
        self.duration -= 1
        self.ice_cooldown = random.randint(20, 30)
        self.Update_Animation()
        return True

    def Update_Animation(self):
        if self.animation >= self.animation_max:
            self.animation = 0
        else:
            self.animation += 1

        return


    def Update_Light_Level(self):
        pass

    def Ice_Particle_Creation(self):

        speed = 1.2
       
        # Calculate the base angle using atan2(y, x)
        x_direction = random.uniform(-1, 1)
        y_direction = random.uniform(-1, 1)
        base_angle = math.atan2(y_direction, x_direction)

        pos_x = math.cos(base_angle) * speed
        pos_y = math.sin(base_angle) * speed
        direction = (pos_x, pos_y)
        self.ice_shooter.Shoot_Particles(self.entity, 10, direction)

    
    def Render(self, surf, offset=(0, 0)):
        item_image = self.game.assets[self.type][self.animation].convert_alpha()
        item_image.set_alpha(200)

        
        # Render the cloud
        surf.blit(item_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    
    