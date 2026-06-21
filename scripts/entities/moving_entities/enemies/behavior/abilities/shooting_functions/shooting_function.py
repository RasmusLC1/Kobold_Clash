import pygame
class Shooting_Function():
    def __init__(self, game):
        self.game = game

    def Initialise_Shooting(self, entity):
        entity.Set_Target(self.game.player.pos)

        attack_direction = self.Set_Attack_Direction(entity)

        if not attack_direction:
            return None
        
        return attack_direction

    def Set_Attack_Direction(self, entity):
        attack_direction = pygame.math.Vector2(entity.target[0] - entity.pos[0], entity.target[1] - entity.pos[1])
        if not attack_direction:
            return (0,0)
        attack_direction.normalize_ip()
        return attack_direction