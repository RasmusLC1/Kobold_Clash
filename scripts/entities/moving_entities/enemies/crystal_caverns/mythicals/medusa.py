from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.entities.moving_entities.enemies.crystal_caverns.mythicals.minotaur.minotaur_intent_manager import Minotaur_Intent_Manager
from scripts.engine.keys.keys import keys
import pygame

ICE_PROJECTILE_NUM = 3 * 20
CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX = 1 # heals 1 health every second

class Medusa(Enemy):

    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.medusa, health, strength, max_speed, agility, intelligence, stamina, 0.9, keys.mythical, 100, size = (64, 64))
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(5)
        self.intent_manager.Set_Intent([keys.direct, keys.attack])
        self.intent_manager.Set_Intent_Cooldown_Max(120)
        self.last_health_index = self.Calculate_Health_Index(self.health)
        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.slash, 5)


    def Update(self, tilemap, delta_time, movement=...):
        self.Enrage()
        return super().Update(tilemap, delta_time, movement)


    def Enrage(self):
        current_index = self.Calculate_Health_Index(self.health)
        if current_index < self.last_health_index:
            # Lost a bucket → enrage once
            self.Set_Strength(self.strength + 1)
            self.last_health_index = current_index

    # Cap the strength gain to +5
    def Calculate_Health_Index(self, health):
        health_fraction = health / self.max_health
        health_index = max(-1, min(int((1 - health_fraction) * 5), 5))  # Invert fraction and scale to index range
        return health_index

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