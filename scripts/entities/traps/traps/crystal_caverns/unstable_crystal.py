from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.magic_attacks.fire.fire_explosion import Fire_Explosion
import pygame

CLATTER_RANGE = 500
DEFAULT_TRIGGER_RADIUS = 32  # Pixels padded around each side of the crystal

class Unstable_Crystal(Trap):
    def __init__(self, game, pos):
        self.trigger_radius = DEFAULT_TRIGGER_RADIUS
        self.damage = 5
        super().__init__(game, pos, keys.unstable_crystal)
        self.Add_Light()


    # Expanded rect using the trigger radius
    def rect(self):
        return pygame.Rect(
            self.pos[0] - self.trigger_radius,
            self.pos[1] - self.trigger_radius,
            self.size[0] + (self.trigger_radius * 2),
            self.size[1] + (self.trigger_radius * 2)
        )

    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return
        
        self.Generate_Sound(keys.fire_explosion, 0.3, CLATTER_RANGE)
        
        # Spawn explosion at crystal location
        fire_explosion = Fire_Explosion(self.game, self.pos, self.damage)
        self.game.item_handler.Add_Item(fire_explosion)
        
        # Safe removal via trap handler
        self.game.trap_handler.Remove_Trap(self)

    def Add_Light(self):
        self.light_source = self.game.light_handler.Add_Light(self.pos, self.light_strength, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)