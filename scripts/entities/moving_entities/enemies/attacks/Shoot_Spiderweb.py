from scripts.entities.items.weapons.projectiles.spider_web_projectile import Spider_Web_Projectile
import pygame
from scripts.engine.keys.keys import keys

class Shoot_Spiderweb():
    def __init__(self, game):
        self.game = game

    def Initialise_Spider_Web(self, entity):
        entity.Set_Target(self.game.player.pos)

        attack_direction = self.Set_Attack_Direction(entity)

        if not attack_direction:
            return
        

        damage = 1
        speed = 1
        max_range = 280

        spider_web = Spider_Web_Projectile(self.game,
                                    entity.rect(),
                                    keys.spider_web,
                                    damage,
                                    speed,
                                    max_range,
                                    'particle',
                                    80,
                                    attack_direction,  
                                    entity
                                )
        self.game.item_handler.Add_Item(spider_web)


    def Set_Attack_Direction(self, entity):
        attack_direction = pygame.math.Vector2(entity.target[0] - entity.pos[0], entity.target[1] - entity.pos[1])
        if not attack_direction:
            return (0,0)
        attack_direction.normalize_ip()
        return attack_direction