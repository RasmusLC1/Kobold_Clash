import pygame
from scripts.engine.keys.keys import keys


class Attack_Effect_Weapon():
    def __init__(self, game, weapon):
        self.game = game
        self.weapon = weapon
        self.effect_type = None
        self.flip_x = False


    def Init_Attack_Effect_Animation(self):
        self.effect_type = self.weapon.Get_Dominant_Effect() + '_' + self.weapon.active_attack_type + '_' + keys.effect
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
        try:
            attack_effect = self.game.assets[self.effect_type][self.weapon.animation]
        except Exception as e:
            print(f'FAILED TO LOAD ATTACK EFFECT{e}', self.effect_type, self.weapon.animation)
            return
        
        original_center = image_rect.center 

        # 2. Scale and Flip the image
        scaled_image = pygame.transform.scale_by(attack_effect, 2.0) # Example scale
        final_image = pygame.transform.flip(scaled_image, flip_x, False)

        # 3. Create a NEW rect from the new image size
        image_rect = final_image.get_rect()

        # 4. Move the new rect so its center matches the original center
        image_rect.center = original_center

        # 5. Blit using the updated rect
        surf.blit(final_image, image_rect)
    
    def Set_Attack_Effect_Animation(self, state):
        self.attack_effect_animation = state
    
    def Set_Attack_Effect_Animation_Counter(self, state):
        self.attack_effect_animation_counter = state