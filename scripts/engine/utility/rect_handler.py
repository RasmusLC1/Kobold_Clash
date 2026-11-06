import pygame
HITBOX_COLOUR = (0, 255, 0)

class Rect_Handler():
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

    def rect(self, pos):
        pos_x, pos_y = self.Calculate_Rect_Pos(pos)
        return pygame.Rect(pos_x, pos_y, self.size_x, self.size_y)

    def Calculate_Rect_Pos(self, pos):
        pos_x = pos[0]
        pos_y = pos[1]
        return pos_x, pos_y

    def Render_Hitbox(self, pos, surf, offset):
        rect = self.rect(pos).move(-offset[0], -offset[1])
        pygame.draw.rect(surf, HITBOX_COLOUR, rect, 1)