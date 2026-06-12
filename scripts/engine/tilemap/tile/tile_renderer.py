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
            # Fetch base asset safely
            base_asset = self.tile.game.assets[self.tile.sub_type][self.tile.variant]
            # FORCE standard assets to support alpha channels cleanly in memory
            self.sprite = base_asset.convert_alpha()
            self.rendered_surface = self.sprite.copy()
        except Exception:
            self.sprite = None
            self.rendered_surface = None

    def Update_Surface(self):
        if not self.sprite:
            return
            
        self.rendered_surface = self.sprite.copy()
        
        # Scale variables down cleanly within the matching 0-255 range
        tile_activeness = max(0, min(255, self.tile.active))
        light = self.tile.lighting.light_level
        
        # Calculate smooth visibility steps
        tile_darken_factor = min(255, (255 * (1.0 - math.exp(-tile_activeness / 64.0))))
        light_level = min(255, light * 25) if light > 0 else 0
        
        final_alpha = max(0, min(255, 220 - tile_darken_factor + light_level))
        inverted_alpha = max(0, min(220, 220 - final_alpha))

        darkening_surface = pygame.Surface(self.rendered_surface.get_size(), flags=pygame.SRCALPHA)
        darkening_surface.fill((0, 0, 0, int(inverted_alpha)))
        
        self.rendered_surface.blit(darkening_surface, (0, 0))
        self.tile.needs_redraw = False
        
    def Render(self, surf, offset):
        if not self.sprite or self.rendered_surface is None:
            return
            
        if self.tile.needs_redraw:
            self.Update_Surface()

        render_pos = (self.render_x - offset[0], self.render_y - offset[1])
        print(render_pos)
        surf.blit(self.rendered_surface, render_pos)