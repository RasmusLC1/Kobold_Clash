import pygame

class Minimap:
    def __init__(self, game, tilemap):
        self.game = game
        self.tilemap = tilemap
        self.tiles = {} 
        self.size = 110 # Square size for a perfect circle
        self.radius = self.size // 2
        
        # Use SRCALPHA to allow transparency
        self.minimap_display = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.zoom = 0.8

    def Clear(self):
        self.tiles.clear()

    def Add_Tile_To_Minimap(self, tile):
        if tile.pos not in self.tiles:
            self.tiles[tile.pos] = tile

    def Render(self, surf):
        # Clear with a transparent background
        self.minimap_display.fill((0, 0, 0, 0)) 
        
        # Draw the dark circular background for the map
        center = (self.radius, self.radius)

        self.Render_Circle(center)


        # Render tiles and player
        p_tile_x = self.game.player.pos[0] / self.tilemap.tile_size
        p_tile_y = self.game.player.pos[1] / self.tilemap.tile_size
        self.Render_Tiles(p_tile_x, p_tile_y, center[0], center[1])
        pygame.draw.circle(self.minimap_display, (50, 255, 50), center, 3)

        
        # blit to screen
        padding = 5
        pos_x = self.game.screen_width // self.game.render_scale - padding - self.size
        pos_y = padding
        surf.blit(self.minimap_display, (pos_x, pos_y))

    def Render_Circle(self, center):
        pygame.draw.circle(self.minimap_display, (20, 20, 20, 180), center, self.radius)

        # This surface is solid, and we will cut a hole in it
        mask = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        mask.fill((255, 255, 255, 255)) # Fill with solid white
        
        # Cut a hole in the mask (everything inside this circle becomes transparent on the mask)
        pygame.draw.circle(mask, (0, 0, 0, 0), center, self.radius)
        
        # Use BLEND_RGBA_SUB to subtract the solid white corners of the mask from your minimap
        # This keeps the center (where the mask is 0) and erases the corners
        self.minimap_display.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        

    def Render_Tiles(self, p_tile_x, p_tile_y, center_x, center_y):
        radius_sq = (self.radius) ** 2 # Use squared radius to avoid slow sqrt()
        
        for pos, tile in self.tiles.items():
            render_x = (pos[0] - p_tile_x) * self.zoom + center_x
            render_y = (pos[1] - p_tile_y) * self.zoom + center_y

            # Check if point is inside circle: (x-cx)^2 + (y-cy)^2 < r^2
            dist_sq = (render_x - center_x)**2 + (render_y - center_y)**2
            
            if dist_sq < radius_sq:
                tile.Render_Minimap(self.minimap_display, (render_x, render_y))