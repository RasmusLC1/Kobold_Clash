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
            self.sprite = self.game.assets[self.sub_type][self.variant].copy()
        except Exception as e:
            return

    def Update_Surface(self):
        if not self.sprite:
            return

        # Get the tile surface from the assets
        self.rendered_surface = self.sprite.copy()
        # Adjust the tile activeness calculation
        tile_activeness = max(0, min(255, 700 - self.active))
        
        # Apply a non-linear scaling for a smoother transition
        tile_darken_factor = min(255, (255 * (1 - math.exp(-tile_activeness / 255)) + 150))
        light_level = self.tile.lightlevel
        if light_level > 0:
            light_level = min(255, light_level * 25)
        else:
            light_level = 1
        tile_darken_factor = max(0, min(220, tile_darken_factor - light_level))

        # Create a darkening surface with an alpha channel
        darkening_surface = pygame.Surface(self.rendered_surface.get_size(), flags=pygame.SRCALPHA)
        darkening_surface.fill((0, 0, 0, int(tile_darken_factor)))
        
        # Blit the darkening surface onto the tile surface
        self.rendered_surface.blit(darkening_surface, (0, 0))

        self.tile.needs_redraw = False  # Reset flag
        
    def Render(self, surf, offset):
        if not self.sprite or self.rendered_surface is None:
            return
            
        if self.tile.needs_redraw:
            self.Update_Surface()

        render_pos = (self.render_x - offset[0], self.render_y - offset[1])
        surf.blit(self.rendered_surface, render_pos)