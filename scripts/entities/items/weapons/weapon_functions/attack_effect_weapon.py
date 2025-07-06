import pygame
from scripts.engine.keys.keys import keys


class Attack_Effect_Weapon():
    def __init__(self, game, weapon):
        self.game = game
        self.weapon = weapon
        self.effect_type = None
        self.attack_effect_animation = 0 # current effect animation frame
        self.attack_effect_animation_max = 6 # Amount of effect animation frames
        self.attack_effect_animation_time = 0 # Time it takes to change between frames
        self.attack_effect_animation_counter = 0 # Animation countdown that ticks up to time

        self.special_attack_effect_animation_max = 1 # Maximum amount of attack animations



    def Update_Attack_Effect_Animation(self):
        if self.attack_effect_animation_counter >= self.attack_effect_animation_time:
            self.attack_effect_animation_counter = 0
            self.attack_effect_animation = min(self.attack_effect_animation + 1, self.attack_effect_animation_max)
            return
        self.attack_effect_animation_counter += 1

    
     # Used to update special attack animations, not the effect itself
    def Update_Special_Attack_Effect_Animation(self):
        if self.attack_effect_animation_counter >= self.attack_effect_animation_time:
            self.attack_effect_animation_counter = 0
            self.attack_effect_animation = min(self.attack_effect_animation + 1, self.special_attack_effect_animation_max)
            return

        self.attack_effect_animation_counter += 1


    def Init_Attack_Effect_Animation(self):
        self.effect_type = self.weapon.Get_Dominant_Effect() + '_' + self.weapon.attack_type + '_' + keys.effect
        self.attack_effect_animation_time = self.weapon.entity_attack_type.attacking / self.attack_effect_animation_max

    def Set_Special_Attack_Effect_Animation_Time(self):
        self.attack_effect_animation_time = self.weapon.special_attack / self.special_attack_effect_animation_max


    def Reset_Attack_Effect_Animation(self):
        self.attack_animation_counter = 0
        self.attack_effect_animation_time = 0
        self.attack_effect_animation = 0

    

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
    def Render_Attack_Effect(self, surf, offset):
        if not self.weapon.entity_attack_type.attacking:
            return
        pos = self.Attack_Effect_Position(offset)
        attack_effect = self.game.assets[self.effect_type][self.attack_effect_animation]
        # attack_effect.set_alpha()
        attack_effect = pygame.transform.rotate(attack_effect, self.weapon.rotate)
        surf.blit( pygame.transform.flip(attack_effect, self.weapon.flip_x, False), (pos[0], pos[1]))

    
    def Set_Attack_Effect_Animation(self, state):
        self.attack_effect_animation = state
    
    def Set_Attack_Effect_Animation_Counter(self, state):
        self.attack_effect_animation_counter = state