from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.magic_attacks.fire.fire_explosion import Fire_Explosion
from .crystal_cavern_registry import register_trap
import pygame
import random

CLATTER_RANGE = 500
DEFAULT_TRIGGER_RADIUS = 10  # Pixels padded around each side of the crystal

# Mimics a normal light crystal but explodes if you get to close
@register_trap(keys.unstable_crystal, 10.1)
class Unstable_Crystal(Trap):
    def __init__(self, game, pos):
        self.trigger_radius = DEFAULT_TRIGGER_RADIUS
        self.warning_radius = DEFAULT_TRIGGER_RADIUS * 10
        self.damage = 5
        self.center = pos
        version = random.randint(1, 5)
        rendered_image = str(keys.glowing_crystal) + '_' + str(version)
        super().__init__(game, pos, rendered_image, max_animation=5,
                         animation_cooldown_max=1.2)
        self.light_strength = 9
        self.Add_Light()


    def Update(self, delta_time):
        self.Check_Player_Distance()
        return super().Update(delta_time)

    # Visual indicator that the crystal is unstable
    def Check_Player_Distance(self):
        if not self.Twitch():
            return
        
        self.Check_If_Explode()

    def Twitch(self):
        player = self.game.player
        if player.Get_Effect(keys.silence): # Silent player does not disrupt crystal
            return False
        if not player.rect().colliderect(self.warning_rect()):
            return False
        new_x_pos = self.center[0] + random.randint(-1, 1)
        new_y_pos = self.center[1] + random.randint(-1, 1)
        self.Set_Position((new_x_pos, new_y_pos))
        return True

    # Expanded rect using the trigger radius
    def rect(self):
        return pygame.Rect(
            self.pos[0] - self.trigger_radius,
            self.pos[1] - self.trigger_radius,
            self.size[0] + (self.trigger_radius * 2),
            self.size[1] + (self.trigger_radius * 2)
        )

    def warning_rect(self):
        return pygame.Rect(
            self.pos[0] - self.warning_radius,
            self.pos[1] - self.warning_radius,
            self.size[0] + (self.warning_radius * 2),
            self.size[1] + (self.warning_radius * 2)
        )

    def Add_Entity(self, entity):
        pass
    
    def Check_If_Explode(self):
        player = self.game.player

        if not self.rect().colliderect(player.rect()):
            return False
        self.Explode()

    def Explode(self):
        self.Generate_Sound(keys.fire_explosion, 0.3, CLATTER_RANGE)
        
        # Spawn explosion at crystal location
        fire_explosion = Fire_Explosion(self.game, self.pos, self.damage)
        self.game.item_handler.Add_Item(fire_explosion)
        self.game.light_handler.Remove_Light(self.light_source)

        # Safe removal via trap handler
        self.game.trap_handler.Remove_Trap(self)


    def Add_Light(self):
        self.light_source = self.game.light_handler.Add_Light(self.pos, self.light_strength, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)