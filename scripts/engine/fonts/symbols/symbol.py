import pygame

class Symbol:
    def __init__(self, key, sprite, group="effect"):
        self.key = key          # keys.healing, keys.fire_resistance etc
        self.image = sprite     # Pre-extracted or pre-scaled pygame.Surface
        self.group = group      # "effect", "element", "stat", "utility" etc

    def render(self, surf, pos, scale=1.0):
        if scale != 1.0:
            size = (int(self.image.get_width() * scale), int(self.image.get_height() * scale))
            scaled_img = pygame.transform.scale(self.image, size)
            surf.blit(scaled_img, pos)
        else:
            surf.blit(self.image, pos)