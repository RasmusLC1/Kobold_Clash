import pygame
import math

class Tile_Renderer:
    __slots__ = ['tile', 'sprite', 'rendered_surface', 'render_x', 'render_y']

    def __init__(self, tile):
        self.tile = tile
        self.sprite = None
        self.rendered_surface = None
        self.render_x = tile.pos[0] * tile.size
        self.render_y = tile.pos[1] * tile.size
        self.Set_Sprite()

    def Set_Sprite(self):
        try:
            # Safely fetch base asset
            self.sprite = self.tile.game.assets[self.tile.sub_type][self.tile.variant].copy()
            # FIXED: Ensure the cache surface is instantiated immediately alongside base sprite
            if self.sprite:
                self.rendered_surface = self.sprite.copy()
        except Exception:
            self.sprite = None
            self.rendered_surface = None

    def Update_Surface(self):
        if not self.sprite:
            return
            
        # Re-initialize current image layer frame
        self.rendered_surface = self.sprite.copy()
        
        # FIXED: Balanced decay calculation to prevent alpha saturation loops
        tile_activeness = max(0, min(255, self.tile.active))
        
        # Exponential curve now accurately tracks visibility steps
        tile_darken_factor = min(255, (255 * (1.0 - math.exp(-tile_activeness / 64.0))))
        
        # Incorporate light calculation levels safely
        light = self.tile.lighting.light_level
        light_level = min(255, light * 25) if light > 0 else 0
        
        # Final surface alpha composition level calculation
        final_alpha = max(0, min(255, 220 - tile_darken_factor + light_level))
        # Invert balance step to ensure light decreases total darkness factor
        inverted_alpha = max(0, min(220, 220 - final_alpha))

        # Create alpha masking surface overlay
        darkening_surface = pygame.Surface(self.rendered_surface.get_size(), flags=pygame.SRCALPHA)
        darkening_surface.fill((0, 0, 0, int(inverted_alpha)))
        
        self.rendered_surface.blit(darkening_surface, (0, 0))
        self.tile.needs_redraw = False

    def Render(self, surf, offset):
        if not self.sprite or self.rendered_surface is None:
            return
            
        if self.tile.needs_redraw:
            self.Update_Surface()
            
        surf.blit(self.rendered_surface, (self.render_x - offset[0], self.render_y - offset[1]))


