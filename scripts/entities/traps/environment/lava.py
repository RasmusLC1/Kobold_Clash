from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

import random

# TODO: General rewrite for the update logic
class Lava(Trap):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
        self.animation = random.randint(0, 2)
        self.light_level = 10
        self.light_source = self.game.light_handler.Add_Light(self.pos, self.light_level, self.tile)
        self.fire_particle_cooldown = 0
        self.slow_amount = 4
        
        

    def Update(self, delta_time):
        if not super().Update(delta_time):
            return False

        if not self.Update_Cooldown(delta_time):
            return
        self.Update_Trapped_Entities()
        return True


    def Update_Trapped_Entities(self):
        for entity in self.entities:
            if not self.rect().colliderect(entity.rect()):
                self.entities.remove(entity)
                entity.Remove_Effect(keys.slow, self.slow_amount)
                continue
            
            if entity.effects.invulnerable.effect:
                return
            if entity.effects.wet.effect:
                entity.effects.wet.Decrease_Effect()
            entity.Damage_Taken(5, (keys.fire, 3))

    def Add_Entity_To_Trap(self, entity):
        if not super().Add_Entity_To_Trap(entity):
            return False
        entity.Set_Effect(keys.slow, self.slow_amount)
        return True


    def Animation_Update(self, delta_time):
        self.Spawn_Fire_Particle(delta_time)

        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
            return

        
        if self.animation >= 2:
            self.animation = 0
        else:
            self.animation += 1
        
        self.animation_cooldown = random.uniform(0.4, 0.5)

    def Spawn_Fire_Particle(self, delta_time):
        if not self.fire_particle_cooldown:
            self.fire_particle_cooldown = random.uniform(1, 2)
            self.game.particle_handler.Activate_Particles(random.randint(1, 2), keys.fire_particle, self.rect().center)

            return
        
        self.fire_particle_cooldown -= delta_time
        return