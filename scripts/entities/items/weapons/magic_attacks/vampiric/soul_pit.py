from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_explosion import Elemental_Explosion
import pygame
from scripts.engine.keys.keys import keys


class Soul_Pit(Elemental_Explosion):
    def __init__(self, game, pos, power, entity = None):
        super().__init__(game, keys.soul_pit, keys.vampiric, pos, power, 5, 5, 5, entity)
        # extend duration, lower damage and increase range
        self.delete_countdown *= 3
        self.damage = max(1, self.damage // 10)
        self.damage_range = power
        self.power *= 2

    def Compute_Damage(self, entity):
        if entity.damage_cooldown:
            return
        distance = self.Distance(self.pos, entity.pos)
        if distance > self.damage:
            return
        damage = round(max(1, min(30, self.damage * 5 - distance)))
        entity.Damage_Taken(damage, (self.effect_type, 0))
        if self.effect:
            entity.Set_Effect(self.effect, self.effect_strength)

    def Pull_Enemies_In(self):
        for entity in self.nearby_entities:
            direction_vector = pygame.math.Vector2(self.pos) - pygame.math.Vector2(entity.pos)
            if direction_vector.length() < 0:
                return
            if direction_vector:
                direction_vector.normalize_ip()
            # Move entities towards 
            entity.Set_Frame_movement((direction_vector[0] * 2, direction_vector[1] * 2))
            entity.Tile_Map_Collision_Detection(self.game.tilemap)

    def Update_Animation(self, delta_time):
        self.Pull_Enemies_In()
        for entity in self.nearby_entities:
            self.Compute_Damage(entity)
        return super().Update_Animation(delta_time)