from scripts.entities.items.weapons.projectiles.spider_web_projectile import Spider_Web_Projectile
from scripts.entities.moving_entities.enemies.behavior.abilities.shooting_functions.shooting_function import Shooting_Function

import pygame
from scripts.engine.keys.keys import keys

class Shoot_Spiderweb(Shooting_Function):
    def __init__(self, game):
        self.game = game

    def Initialise_Shooting(self, entity):
        attack_direction =  super().Initialise_Shooting(entity)

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


