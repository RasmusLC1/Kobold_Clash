import pygame
from scripts.entities.entity.entities import PhysicsEntity
from scripts.engine.keys.keys import keys
import random


class Decoration(PhysicsEntity):
    def __init__(self, game, type, pos, size, destructable = False, health = 0,
                 destruction_sound = None, destruction_clatter = 500,
                 animation = 0, max_animation = 0, animation_cooldown_max = 0) -> None:
        # Version 0 indexed
        self.animation = animation
        self.max_animation = max_animation
        super().__init__(game, type, keys.decoration, pos, size,
                         max_animation=max_animation,
                         animation_cooldown_max=animation_cooldown_max)
        self.game.tilemap.Add_Entity_To_Tile(self.tile, self)
        self.light_level = 10
        self.destructable = destructable
        self.health = health
        self.empty = False
        self.destruction_sound = destruction_sound
        self.destruction_clatter_range = destruction_clatter
        self.Set_Sprite()


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['animation'] = self.animation
        self.saved_data['empty'] = self.empty

    def Load_Data(self, data):
        self.Set_Animation(data['animation'])
        self.empty = data['empty']
        return super().Load_Data(data)

    def Update_Animation(self, delta_time):
        pass

    def Open(self, generate_clatter = False):
        pass

    def Set_Animation(self, animation_state):
        self.animation = min(animation_state, self.max_animation)
        self.Set_Entity_Image()


    def Increase_Animation(self):
        self.animation += 1
        if self.animation > self.max_animation:
            self.animation = 0
        self.Set_Entity_Image()

    
    def Damage_Taken(self, damage, effect):
        if not self.health:
            return

        # Double damage for blunt weapons
        if effect == 'blunt':
            damage *= 2
        self.game.particle_handler.Activate_Particles(random.randint(2, 4), keys.loot_particle, self.rect().center)

        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.Destroyed()
        
    def Destroyed(self):
        if self.health > 0:
            return False
        self.game.decoration_handler.Remove_Decoration(self)
        
        self.Generate_Sound(self.destruction_sound, 0.2, self.destruction_clatter_range)
        self.game.particle_handler.Activate_Particles(random.randint(10, 15), keys.loot_particle, self.rect().center)
        return True
        
    def Spawn_Reward(self, item):
        pass

