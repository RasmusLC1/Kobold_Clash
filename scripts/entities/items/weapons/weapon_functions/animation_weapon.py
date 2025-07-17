import pygame
from scripts.engine.keys.keys import keys
import random


class Animation_Weapon():
    def __init__(self, game, weapon, attack_animation_max):
        self.game = game
        self.weapon = weapon
        self.animation_cooldown = self.weapon.animation_cooldown
        self.animation_cooldown_max = self.weapon.animation_cooldown_max
        self.max_animation = self.weapon.max_animation
        self.attack_type = self.weapon.attack_type


        self.attack_animation = 0 # Current attack animation
        self.attack_animation_max = attack_animation_max # Maximum amount of attack animations
        self.attack_animation_time = 0 # Time to shift to new animation
        self.attack_animation_counter = 0 # Animation countdown that ticks up to time



    def Update_Animation(self, delta_time):
        if not self.weapon.equipped:
            return
        if self.animation_cooldown:
            self.animation_cooldown -= delta_time
        else:
            self.animation_cooldown = self.animation_cooldown_max
            self.animation = random.randint(0,self.max_animation)

    def Update_Attack_Animation(self):
        if not self.weapon.entity_attack_type:
            print("ATTACK TYPE MISSING WEAPON ", self.weapon.entity.type)
            return
        
        if self.weapon.entity_attack_type.Reset_Attack():
            return
        self.animation = self.attack_animation
        self.sub_type = self.weapon.type + '_attack_' + self.attack_type
        self.attack_animation_counter += 1
        if self.attack_animation_counter >= self.attack_animation_time:
            self.attack_animation_counter = 0
            self.attack_animation += 1
            if self.attack_animation > self.attack_animation_max:
                self.attack_animation = 0
        return
    
    def Enemy_Shooting_Animation(self):
        if self.attack_animation_time <= self.attack_animation_counter:
            self.attack_animation_counter = 0
            self.attack_animation = min(self.attack_animation_max, self.attack_animation + 1)
    
    def Reset_Animation(self):
        self.attack_animation = 0

    def Set_Attack_Animation_Time(self):
        self.attack_animation_time = int(self.weapon.attacking / self.attack_animation_max)
