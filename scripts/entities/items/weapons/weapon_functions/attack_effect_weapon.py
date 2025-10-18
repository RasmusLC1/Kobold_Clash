import pygame
from scripts.engine.keys.keys import keys


class Attack_Effect_Weapon():
    def __init__(self, game, weapon):
        self.game = game
        self.weapon = weapon
        self.effect_type = None
        self.flip_x = False


    def Init_Attack_Effect_Animation(self):
        self.effect_type = self.weapon.Get_Dominant_Effect() + '_' + self.weapon.attack_type + '_' + keys.effect
        self.flip_x != self.weapon.flip_x


    # Handle computing the weapon's attack effect position
    def Attack_Effect_Position(self, offset):
        entity = self.weapon.entity
        pos_x = entity.pos[0] - offset[0]
        pos_y = entity.pos[1] - offset[1] - 30
        if entity.attack_direction[0] < 0:
            pos_x += entity.attack_direction[0] * 50
        else:
            pos_x += entity.attack_direction[0] * 10
        
        if entity.attack_direction[1] < 0:
            pos_y += entity.attack_direction[1] * 20
        else:
            pos_y += entity.attack_direction[1] * 30

        return (pos_x, pos_y)

   
    # Handle rendering the weapons attack effect
    def Render_Attack_Effect(self, surf, image_rect, flip_x):
        if self.weapon.entity_attack_type.attacking <= 0 or not self.effect_type:
            return
        
        # TODO: ANIMATION VALUE IS UPDATED NEED TO FIND WHERE
        print(self.effect_type, self.weapon.animation, self.weapon.entity.animation_handler.animation)
        attack_effect = self.game.assets[self.effect_type][self.weapon.animation]
        # attack_effect.set_alpha()
        # attack_effect = pygame.transform.rotate(attack_effect, self.weapon.rotate)
        surf.blit( pygame.transform.flip(attack_effect, flip_x, False), image_rect)

    
    def Set_Attack_Effect_Animation(self, state):
        self.attack_effect_animation = state
    
    def Set_Attack_Effect_Animation_Counter(self, state):
        self.attack_effect_animation_counter = state