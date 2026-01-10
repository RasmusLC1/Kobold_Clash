from scripts.engine.keys.keys import keys

import random
import json
import pygame
import math
import copy

class Minimap:
    def __init__(self, game, tilemap):
        self.game = game
        self.tilemap = tilemap
        self.tiles = {} 
        # Create a surface with a fixed size for the UI
        self.width = 150
        self.height = 100
        self.minimap_display = pygame.Surface((self.width, self.height))
        self.zoom = 1 # Pixels per tile coordinate

    def Clear(self):
        self.tiles.clear()

    def Add_Tile_To_Minimap(self, tile):
        # Fixed logic: self.tiles[key] = tile
        if tile.pos not in self.tiles:
            self.tiles[tile.pos] = tile

    def Render(self, surf):
        # 1. Clear the surface (maybe with a semi-transparent background)
        self.minimap_display.fill((20, 20, 20, 150)) 
        game = self.game
        player_pos = game.player.pos

        # 2. Calculate offset to center map on player
        # player_pos is usually in world coords (pixels), convert to tile coords
        p_tile_x = player_pos[0] / self.tilemap.tile_size
        p_tile_y = player_pos[1] / self.tilemap.tile_size

        # Offset puts the player at the center of the minimap surface
        center_x, center_y = self.width // 2, self.height // 2

        self.Render_Tiles(p_tile_x, p_tile_y, center_x, center_y)

        # 3. Draw a dot for the player at the exact center
        pygame.draw.circle(self.minimap_display, (50, 255, 50), (center_x, center_y), 2)

        padding = 5
        pos_x = game.screen_width // game.render_scale - padding - self.width
        pos_y = padding

        surf.blit(self.minimap_display, (pos_x, pos_y))

    def Render_Tiles(self, p_tile_x, p_tile_y, center_x, center_y):
        for pos, tile in self.tiles.items():
            # Calculate position on the minimap relative to player
            # (TilePos - PlayerPos) * Zoom + HalfSurface
            render_x = (pos[0] - p_tile_x) * self.zoom + center_x
            render_y = (pos[1] - p_tile_y) * self.zoom + center_y

            # Only render if the tile is actually inside the minimap box
            if 0 <= render_x < self.width and 0 <= render_y < self.height:
                tile.Render_Minimap(self.minimap_display, (render_x, render_y))