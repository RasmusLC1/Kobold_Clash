from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.entities.moving_entities.enemies.crystal_caverns.mythicals.medusa.medusa_animation_handler import Medusa_Animation_Handler
from scripts.engine.keys.keys import keys
import pygame

RANGED_DISTANCE = 100
ATTACK_TYPE_COOLDOWN = 0.5 # heals 1 health very second

class Medusa(Enemy):

    _animation_handler = Medusa_Animation_Handler 

    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.medusa, health, strength, max_speed, agility, intelligence, stamina, 0.9, keys.mythical, 100, size = (64, 64))
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(5)
        self.intent_manager.Set_Intent([keys.direct, keys.attack])
        self.intent_manager.Set_Intent_Cooldown_Max(120)
        self.last_health_index = self.Calculate_Health_Index(self.health)
        self.attack_type_cooldown = 0
        self.attack_type = keys.range
        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.slash, 5)


    def Update(self, tilemap, delta_time, movement=...):
        self.Set_Attack_Type(delta_time)
        return super().Update(tilemap, delta_time, movement)

    # Set the attack type based on player distance
    def Set_Attack_Type(self, delta_time):
        if self.attack_type_cooldown > 0:
            self.attack_type_cooldown -= delta_time
            return
        
        self.attack_type_cooldown = ATTACK_TYPE_COOLDOWN
        if self.distance_to_player > RANGED_DISTANCE:
            self.attack_type = keys.range
        else:
            self.attack_type = keys.direct

    def Ranged_Attack(self):
        pass

    def Attack(self, delta_time):
        if self.attack_type == keys.direct:
            return super().Attack(delta_time)
        else:
            return self.Ranged_Attack()

    # Custom render function to account for large attack animations
    def Render(self, surf, offset=(0, 0)):
        if not self.active or not self.Update_Light_Level():
            return False
        if not self.animation_handler.entity_image:
            return False

        self.Update_Dark_Surface()

        # Get the larger sprite
        image = pygame.transform.flip(self.rendered_image, self.flip[0], False)
        image_rect = image.get_rect(center=(self.pos[0] - offset[0] + self.size[0] // 2,
                                            self.pos[1] - offset[1] + self.size[1] // 2))

        # Draw it centered around Medusa's logic/collision box
        surf.blit(image, image_rect.topleft)

        # Draw effects (like damage flash, poison, etc.)
        self.effects.Render_Effects(surf, offset)
        self.Render_Damage(surf, offset)

        return True