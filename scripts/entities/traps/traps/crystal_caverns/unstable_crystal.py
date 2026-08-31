from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.magic_attacks.fire.fire_explosion import Fire_Explosion
from .crystal_cavern_registry import register_trap
import pygame
import random

CLATTER_RANGE = 500
DEFAULT_TRIGGER_RADIUS = 64  # Pixels padded around each side of the crystal

# Mimics a normal light crystal but explodes if you get to close
@register_trap(keys.unstable_crystal, 0.1)
class Unstable_Crystal(Trap):
    def __init__(self, game, pos):
        self.trigger_radius = DEFAULT_TRIGGER_RADIUS
        self.warning_radius = DEFAULT_TRIGGER_RADIUS * 3
        self.damage = 5
        self.center = pos
        super().__init__(game, pos, keys.glowing_crystal, max_animation=5,
                         animation_cooldown_max=1.2)
        self.light_strength = 9
        self.Add_Light()


    def Update(self, delta_time):
        self.Twitch()
        return super().Update(delta_time)

    # Visual indicator that the crystal is unstable
    def Twitch(self):
        if not self.game.player.rect().colliderect(self.warning_rect()):
            return
        new_x_pos = self.center.x + random.randint(-1, 1)
        new_y_pos = self.center.y + random.randint(-1, 1)
        self.Set_Position((new_x_pos, new_y_pos))

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

    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return
        
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