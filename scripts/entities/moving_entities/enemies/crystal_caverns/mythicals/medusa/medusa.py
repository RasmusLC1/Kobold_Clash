from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.entities.moving_entities.enemies.crystal_caverns.mythicals.medusa.medusa_animation_handler import Medusa_Animation_Handler
from scripts.entities.items.weapons.magic_attacks.electric.electric_shooter import Electric_Shooter
from scripts.engine.keys.keys import keys
import pygame

RANGED_DISTANCE = 100
ATTACK_TYPE_COOLDOWN = 0.5 # heals 1 health very second

class Medusa(Enemy):

    _animation_handler = Medusa_Animation_Handler 

    def __init__(self, game, pos):
        super().__init__(game, pos, keys.medusa)
        self.attack_type = keys.range
        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.slash, 5)
        self.electric_damage = 15
        self.ranged_weapon = Electric_Shooter(self.game, self)



    def Update(self, tilemap, delta_time, movement=...):
        # self.Set_Attack_Type(delta_time)
        return super().Update(tilemap, delta_time, movement)

    # Set the attack type based on player distance
    def Set_Attack_Type(self, delta_time):
        if self.attack_type_cooldown > 0:
            self.attack_type_cooldown -= delta_time
            return
        
        self.attack_type_cooldown = ATTACK_TYPE_COOLDOWN
        self.attack_type_cooldown = ATTACK_TYPE_COOLDOWN
        # ranged attack
        if self.distance_to_target > RANGED_DISTANCE and self.attack_type != keys.range:
            self.attack_distance  = 150

        # Direct attack
        elif self.attack_type != keys.direct:
            self.attack_distance  = self.size[0] * 2


    def Trigger_Ranged_Attack(self):
        self.Set_Target()
        self.Set_Attack_Direction()
        self.ranged_weapon.Initialise_Shooting(self, 100, self.electric_damage)

    # Custom render function to account for large attack animations
    def Render(self, surf, offset=(0, 0)):
        if not self.active or not self.Update_Light_Level():
            return False
        if not self.animation_handler.entity_image:
            return False

        self.Update_Dark_Surface()

        # Get the larger sprite
        image = pygame.transform.flip(self.rendered_image, self.animation_handler.flip[0], False)
        image_rect = image.get_rect(center=(self.pos[0] - offset[0] + self.size[0] // 2,
                                            self.pos[1] - offset[1] + self.size[1] // 2))

        # Draw it centered around Medusa's logic/collision box
        surf.blit(image, image_rect.topleft)

        # Draw effects (like damage flash, poison, etc.)
        self.effects.Render_Effects(surf, offset)
        self.Render_Damage(surf, offset)

        return True