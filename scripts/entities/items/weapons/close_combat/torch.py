from scripts.entities.items.weapons.weapon import Weapon
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.light_sources.light_sources_registry import Register_Light_Source
from scripts.entities.entity.animation_handlers.fire_animation_handler import Fire_Animation_Handler


@Register_Light_Source(keys.torch, 0.1)
class Torch(Weapon):
    _animation_handler = Fire_Animation_Handler 
    
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.torch, 1, 2, 3, 100, 'one_handed_melee',
                         keys.fire, max_animation=3, animation_cooldown_max=0.5)
        self.light_source = self.game.light_handler.Add_Light(self.pos, 8, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)
        self.flame_thrower = Flame_Thrower(self.game, None)
        self.fire_charge_max = 2

    def Update(self, delta_time, offset=None):
        self.flame_thrower.Update(delta_time)
        return super().Update(delta_time, offset)
    
    def Render_Floor(self, surf, offset=(0, 0)):
        self.Update_Light_Level()  
        self.Update_Dark_Surface()

        
        if not self.rendered_image:
            self.Set_Sprite()
            if not self.rendered_image:
                self.broken_rendering_counter += 1
                if self.broken_rendering_counter >= 10:
                    self.Delete_Item()
                return

        self.broken_rendering_counter = 0  # reset once a good frame lands
        surf.blit(self.rendered_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    # Pick up the torch and update the general light in the area
    def Pick_Up(self):
        if not super().Pick_Up():
            return
        self.game.light_handler.Remove_Light(self.light_source)
    
    def Set_Entity(self, entity):
        self.flame_thrower.Set_Entity(entity)
        return super().Set_Entity(entity)

    def Spawn_Fire_Particle(self):
        self.game.particle_handler.Activate_Particles(random.randint(1, 3), keys.fire_particle, self.rect().center)

    
    def Set_Attack(self):
        if not super().Set_Attack():
            return False
        self.game.sound_handler.Play_Sound(keys.torch_attack, 0.5)
        return True


    def Ability(self):
        if self.special_attack <= 0 or not self.equipped:
            self.Reset_Special_Attack()
            return
        self.special_attack = 0
        self.flame_thrower.Initialise_Shooting(self.entity, self.fire_charge_max, 3)


    def Set_Special_Attack(self, offset = (0,0)):
        super().Set_Special_Attack(offset)

    def Set_Equip(self, state, entity):
        super().Set_Equip(state, entity)

        if state:
            self.game.player.Update_Light_Source(12)
        else:
            self.game.player.Update_Light_Source(self.game.player.default_light_level)
    
    def Update_Light_Level(self):
        return True

    def Place_Down(self):
        # Parent class Place_down function
        if not super().Place_Down():
            return False

        # Set the player light to False to trigger a general update of the light
        # levels around the player and move the torch light to the new location
        self.game.light_handler.Add_Light_Source(self.light_source)
        self.light_source.Move_Light(self.pos, self.tile)
        return True

    def Update_Dark_Surface(self):
        self.rendered_image = self.entity_image