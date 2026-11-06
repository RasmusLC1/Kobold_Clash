from scripts.entities.items.loot.interactive_loot import Interactive_Loot
import pygame
from scripts.engine.keys.keys import keys

class Radius_Effect_Loot(Interactive_Loot):
    def __init__(self, game, type, pos, max_distance, loot_type, radius, amount,
                 rarity_value, max_amount=5, max_animation = 1,
                 animation_cooldown_max=0):
        super().__init__(game, type, pos, max_distance, (16, 16),
                         loot_type=loot_type, rarity_value=rarity_value,
                         amount = amount,max_amount=max_amount,
                         max_animation=max_animation,
                         animation_cooldown_max=animation_cooldown_max)
        self.radius = radius
        self.Set_Radius_Image()
 
    # Setting the radius image and scaling it
    def Set_Radius_Image(self):
        sprite = self.game.assets['radius']
        item_image = sprite[0].convert_alpha()
        range = self.radius * self.game.tilemap.tile_size
        self.radius_image = pygame.transform.scale(item_image, (range, range))

    # Render the range of the effect
    def Render_Radius(self, surf, offset):
        radius_image = self.radius_image.copy()
        if self.distance_to_player > self.max_distance:
            radius_image.set_alpha(200)
        game = self.game
        range = self.radius * self.game.tilemap.tile_size // 2
        surf.blit(radius_image, (game.mouse.mpos[0] - offset[0] - range, game.mouse.mpos[1] - offset[1] - range))
        
    def Render_Active(self, surf, offset=...):
        if self.clicked:
            self.Render_Radius(surf, offset)
        return super().Render(surf, offset)
    
    # Seperate find enemies close to the mouse
    def Find_Nearby_Entities_Mouse(self):
        self.nearby_entities = self.game.tilemap.Search_Nearby_Tiles(self.radius, self.game.mouse.mpos, keys.enemy, self.ID)

