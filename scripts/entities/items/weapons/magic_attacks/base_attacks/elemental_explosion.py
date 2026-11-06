from scripts.entities.items.item import Item
import pygame
import math
from scripts.engine.keys.keys import keys

class Elemental_Explosion(Item):
    def __init__(self, game, type, effect, pos, power, effect_strength,
                 max_animation, animation_cooldown_max, entity = None):
        super().__init__(game, type, keys.magic_attack, pos,
                         (game.tilemap.tile_size, game.tilemap.tile_size),
                         max_animation=max_animation, animation_cooldown_max=animation_cooldown_max)
        self.entity = entity
        self.delete_countdown = self.max_animation * self.animation_cooldown_max
        self.power = power
        self.damage = power
        self.effect_strength = effect_strength
        self.effect = effect
        self.light_source = self.game.light_handler.Add_Light(self.pos, 4, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)
        self.size = (self.power * self.size[0], self.power * self.size[1])
        self.nearby_entities = []
        self.effect_type = self.effect
        self.Initialise_Explosion()

    def Initialise_Explosion(self):
        self.game.clatter.Generate_Clatter(self.pos, self.effect_strength * 100)

        if not self.Check_Nearby_Entities():
            return

        entity_ID = self.Get_Entity_ID()
        for entity in self.nearby_entities:
            if entity.ID == entity_ID:
                continue
            if not self.Ray_Cast_Towards_Entity(entity):
                continue
            self.Compute_Damage(entity)

    def Check_Nearby_Entities(self):
        self.Find_Nearby_Entities(self.power * 3)
        self.Check_Player_Distance()

        return self.nearby_entities
            

    def Compute_Damage(self, entity):
        distance = self.Distance(self.pos, entity.pos) // self.game.tilemap.tile_size
        damage = round(max(5, min(self.power * 10, self.damage * 10 - distance)))

        entity.Damage_Taken(damage, (self.effect_type, self.damage))
        if self.effect:
            entity.Set_Effect(self.effect, self.effect_strength)

    # Blast hitbox — matches exactly what Render() draws, centered on self.pos
    def Blast_Rect(self):
        half_w = self.size[0] // 2
        half_h = self.size[1] // 2
        return pygame.Rect(
            self.pos[0] - half_w,
            self.pos[1] - half_h,
            self.size[0],
            self.size[1]
        )

    def Check_Player_Distance(self):
        if self.Blast_Rect().colliderect(self.game.player.rect()):
            self.nearby_entities.append(self.game.player)

    def Get_Entity_ID(self):
        if not self.entity:
            return -999
        return self.entity.ID

    # Raycaster to check for line of sight (walls only — range is handled by Blast_Rect)
    def Ray_Cast_Towards_Entity(self, entity):
        start_pos = self.pos
        end_pos = entity.pos

        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)

        if distance == 0:
            return True

        angle = math.atan2(dy, dx)
        step_size = self.game.tilemap.tile_size
        steps = max(1, math.ceil(distance / step_size))

        for i in range(1, steps):
            pos_x = start_pos[0] + math.cos(angle) * step_size * i
            pos_y = start_pos[1] + math.sin(angle) * step_size * i
            pos = (int(pos_x) // step_size, int(pos_y) // step_size)

            if not self.Check_Tile(pos):
                return False

        return True

    def Check_Tile(self, tile_pos):
        tile = self.game.tilemap.Current_Tile(tile_pos)
        if tile:
            if not tile.type:
                print(tile)
                return False
            if tile.physics:
                return False
        return True

    def Update_Animation(self, delta_time, movement=(0, 0)):
        if self.animation >= self.max_animation:
            try:
                self.game.light_handler.Remove_Light(self.light_source)
                del self.light_source
            except Exception:
                pass
            self.game.item_handler.Remove_Item(self)
            return
        super().Update_Animation(delta_time, movement)

    def Render(self, surf, offset=(0, 0)):
        try:
            weapon_image = self.game.assets[self.type][self.animation].convert_alpha()
        except Exception as e:
            print("Explosion renderer", e, self.type, self.animation)

        weapon_image = pygame.transform.scale(weapon_image, self.size)
        width, height = self.size

        x = self.pos[0] - offset[0] - width // 2
        y = self.pos[1] - offset[1] - height // 2

        surf.blit(weapon_image, (x, y))

    def Update_Text_Box(self, hitbox_1, hitbox_2):
        pass

    def Update_Dark_Surface(self):
        if not self.render_needs_update:
            return
        if not self.entity_image:
            return
        self.rendered_image = self.entity_image.copy()

    def Lightup(self, entity_image):
        pass