import pygame
from scripts.engine.assets.keys import keys

class Renderer():
    def __init__(self, game) -> None:
        self.game = game
        self.Update_Background_Image()

    def Update_Background_Image(self):
        self.back_ground_image = pygame.transform.scale(self.game.assets['background'], (self.game.screen_width/self.game.render_scale, self.game.screen_height/self.game.render_scale))

    def Render(self):
        
        render_scroll = self.game.render_scroll
        surf = self.game.display
        surf.blit(self.back_ground_image, (0, 0))
        
        self.game.ray_caster.Ray_Caster()
        self.game.tilemap.Render_Tiles(self.game.ray_caster.tiles, surf, offset=render_scroll)


        self.game.particle_handler.Particle_Render(surf, render_scroll)
        self.game.entities_render.Render(surf, render_scroll)
        self.game.rune_handler.Render_Animation(surf, render_scroll)
        

        self.game.inventory.Render(surf)

        self.game.text_box_handler.Render(surf, render_scroll)
        self.game.player.effects.Render_Effects_Symbols(surf)
        self.game.souls_interface.Render(surf)
        self.game.health_bar.Health_Bar(surf)



    