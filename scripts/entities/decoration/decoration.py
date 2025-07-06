import pygame
from scripts.entities.entities import PhysicsEntity
from scripts.engine.keys.keys import keys
import random


class Decoration(PhysicsEntity):
    def __init__(self, game, type, pos, size, destructable = False, health = 0) -> None:
        super().__init__(game, type, keys.decoration, pos, size)
        self.game.tilemap.Add_Entity_To_Tile(self.tile, self)
        self.light_level = 10
        self.animation = 0
        self.destructable = destructable
        self.health = health
        self.empty = False
        # self.destroyed = False # Flag to prevent 
        self.Set_Sprite()


    def Save_Data(self):
        self.saved_data['animation'] = self.animation
        self.saved_data['empty'] = self.empty
        return super().Save_Data()

    def Load_Data(self, data):
        self.Set_Animation(data['animation'])
        self.empty = data['empty']
        return super().Load_Data(data)

    def Update_Animation(self):
        pass

    def Open(self, generate_clatter = False):
        pass

    def Set_Animation(self, animation_state):
        self.animation = animation_state
        self.Set_Entity_Image()
    
    # Setting the initial sprite type from assets, only called during initial setup
    def Set_Sprite(self):
        self.sprite = self.game.assets[self.type]
        self.Set_Entity_Image()

    # Setting the item image and scaling it
    def Set_Entity_Image(self):
        entity_image = self.sprite[self.animation].convert_alpha()
        self.entity_image = pygame.transform.scale(entity_image, self.size)

    def Damage_Taken(self, damage, effect):
        if not self.health:
            return

        # Double damage for blunt weapons
        if effect == 'blunt':
            damage *= 2
        self.game.particle_handler.Activate_Particles(random.randint(2, 4), keys.loot_particle, self.rect().center, frame=random.randint(10, 20))

        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.Destroyed()
        
    def Destroyed(self):
        if self.health > 0:
            return False
        self.game.decoration_handler.Remove_Decoration(self)
        self.game.clatter.Generate_Clatter(self.pos, 1000) # Generate clatter to alert nearby enemies
        self.game.sound_handler.Play_Sound('chest_break', 0.2)
        self.game.particle_handler.Activate_Particles(random.randint(10, 15), keys.loot_particle, self.rect().center, frame=random.randint(20, 30))
        return True
        
    def Spawn_Reward(self, item):
        pass

    def Render(self, surf, offset = (0,0)):
        if not self.Update_Light_Level():
            return

        
        self.Update_Dark_Surface()

        if not self.rendered_image:
            self.render_needs_update = True
            self.Update_Dark_Surface()
            if not self.rendered_image:
                self.Set_Sprite()
                print(vars(self))
                return
        
        # Render the chest
        surf.blit(self.rendered_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    
