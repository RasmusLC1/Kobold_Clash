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
            self.sprite = self.tile.game.assets[self.tile.sub_type][self.tile.variant].copy()
        except Exception:
            self.sprite = None

    def Update_Surface(self):
        if not self.sprite:
            return
        self.rendered_surface = self.sprite.copy()
        tile_activeness = max(0, min(255, 700 - self.tile.active))
        tile_darken_factor = min(255, (255 * (1 - math.exp(-tile_activeness / 255)) + 150))
        
        light = self.tile.lighting.light_level
        light_level = min(255, light * 25) if light > 0 else 1
        tile_darken_factor = max(0, min(220, tile_darken_factor - light_level))

        darkening_surface = pygame.Surface(self.rendered_surface.get_size(), flags=pygame.SRCALPHA)
        darkening_surface.fill((0, 0, 0, int(tile_darken_factor)))
        self.rendered_surface.blit(darkening_surface, (0, 0))
        self.tile.needs_redraw = False

    def Render(self, surf, offset):
        if not self.sprite:
            return
        if self.tile.needs_redraw:
            self.Update_Surface()
        surf.blit(self.rendered_surface, (self.render_x - offset[0], self.render_y - offset[1]))