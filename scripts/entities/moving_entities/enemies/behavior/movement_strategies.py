import pygame
import random
import math

from scripts.engine.keys.keys import keys

PLAYER_FOUND_MAX = 5

class Movement_Strategies():

    def __init__(self, game, entity) -> None:
        self.game = game
        self.entity = entity

        self.movement_strategy = keys.direct

        self.player_found = 0
        self.player_found_max = 10

        self.line_of_sight_cooldown = 0
        self.direct_pathing_cooldown = 0
        self.target_tile_pos = None
        self.in_range_cooldown = 0
        self.tile_check_timestamp = 0

        # Per-entity approach offset so direct enemies spread out naturally
        self._approach_offset = pygame.math.Vector2(
            random.uniform(-0.4, 0.4),
            random.uniform(-0.4, 0.4)
        )
        self._offset_timer = random.uniform(0, 3)

        self.attack_ranges = {
            keys.long_range:     (200, 160),
            keys.medium_range:   (160, 120),
            keys.short_range:    (120, 80),
            keys.direct:         (48, 0),
            keys.keep_position:  (0, 0),
            keys.idle:           (0, 0),
            keys.run_away:       (1000, 999),
        }

    def Save_Data(self):
        self.entity.saved_data['target_tile_pos'] = self.target_tile_pos
        self.entity.saved_data['movement_strategy'] = self.movement_strategy
        self.entity.saved_data['player_found'] = self.player_found

    def Load_Data(self, data):
        self.target_tile_pos = data['target_tile_pos']
        self.movement_strategy = data['movement_strategy']
        self.player_found = data['player_found']

    # ------------------------------------------------------------------ #
    #  Main entry point called every frame                                 #
    # ------------------------------------------------------------------ #
    def Movement_Strategy(self, delta_time) -> bool:
        if self.entity.distance_to_target > 300:
            return False
        if self.game.player.active_ability == keys.invisibility:
            return False
        if self.entity.active_ability == keys.invulnerable:
            return False
        if not self.Handle_Line_Of_Sight(delta_time):
            return False

        # --- Direct charge: skip tile logic, aim straight at player ---
        if self.movement_strategy == keys.direct:
            self._Direct_Charge(delta_time)
            return True

        # --- Ranged / loiter strategies: tile-based movement ---
        if self.in_range_cooldown > 0:
            self.in_range_cooldown -= delta_time
        else:
            self.Update_Movement_Logic()
        return True

    # ------------------------------------------------------------------ #
    #  Direct charge with per-enemy offset so groups spread out           #
    # ------------------------------------------------------------------ #
    def _Direct_Charge(self, delta_time):
        player_pos = self.game.player.pos
        entity_pos = self.entity.pos

        direction = pygame.math.Vector2(
            player_pos[0] - entity_pos[0],
            player_pos[1] - entity_pos[1],
        )
        if direction.length_squared() == 0:
            return

        direction.normalize_ip()

        # Drift the personal offset slowly so movement stays varied but not jittery
        self._offset_timer -= delta_time
        if self._offset_timer <= 0:
            self._offset_timer = random.uniform(2, 4)
            self._approach_offset = pygame.math.Vector2(
                random.uniform(-0.4, 0.4),
                random.uniform(-0.4, 0.4),
            )

        direction = direction + self._approach_offset
        if direction.length_squared() > 0:
            direction.normalize_ip()

        self.entity.Set_Direction(direction)

    # ------------------------------------------------------------------ #
    #  Tile-based loiter / ranged movement                                 #
    # ------------------------------------------------------------------ #
    def Pathfinding_Cooldown(self, delta_time):
        if self.direct_pathing_cooldown > 0:
            self.direct_pathing_cooldown -= delta_time
            return True
        return False

    def Find_Tile_To_Pathfind_To(self, force_new=False):
        max_range, min_range = self.attack_ranges.get(self.movement_strategy, (0, 0))
        if max_range == 0:
            return None

        entity_dist = self.entity.distance_to_target
        valid_tiles = self.Find_Tiles_In_Range(max_range, min_range, entity_dist)
        if not valid_tiles:
            return None

        if not force_new:
            if not self.Check_In_Range(max_range, min_range, entity_dist):
                return None

        target_tile = random.choice(valid_tiles)
        self.target_tile_pos = target_tile.scaled_pos
        return self.target_tile_pos

    def Check_In_Range(self, max_range, min_range, entity_dist):
        if min_range <= entity_dist <= max_range:
            self.in_range_cooldown = 2.0
            if random.random() < 0.7:   # 70 % chance to hold position
                return False
        return True

    def Find_Tiles_In_Range(self, max_range, min_range, entity_dist):
        surrounding_tiles = self.game.tilemap.Get_Floor_Tiles_Around(self.entity.pos)
        if not surrounding_tiles:
            return []

        player_tile_x = self.game.player.pos[0] // self.game.tilemap.tile_size
        player_tile_y = self.game.player.pos[1] // self.game.tilemap.tile_size

        valid_tiles = [
            tile for tile in surrounding_tiles
            if tile.Get_Distance_To_Player() is not None
            and (tile.scaled_pos[0] != player_tile_x or tile.scaled_pos[1] != player_tile_y)
        ]
        if not valid_tiles:
            return []

        # Too far — pick from the 3 closest tiles for variety
        if entity_dist > max_range:
            sorted_tiles = sorted(valid_tiles, key=lambda t: t.Get_Distance_To_Player())
            return sorted_tiles[:3]

        # Too close — pick from the 3 furthest tiles
        elif entity_dist < min_range:
            sorted_tiles = sorted(valid_tiles, key=lambda t: t.Get_Distance_To_Player(), reverse=True)
            return sorted_tiles[:3]

        # In range — loiter freely
        return valid_tiles

    def Update_Movement_Logic(self):
        entity_pos = self.entity.pos

        if not self.target_tile_pos:
            if not self.Find_Tile_To_Pathfind_To(force_new=False):
                return False

        distance_to_tile = self.Get_Distance(entity_pos, self.target_tile_pos)

        if distance_to_tile < 12:
            if not self.Find_Tile_To_Pathfind_To(force_new=True):
                return False

        self.Calculate_Direction(entity_pos)
        return True

    def Calculate_Direction(self, entity_pos):
        dx = self.target_tile_pos[0] - entity_pos[0]
        dy = self.target_tile_pos[1] - entity_pos[1]

        desired_velocity = pygame.math.Vector2(dx, dy)
        distance = desired_velocity.length()

        if distance > 0:
            desired_velocity = desired_velocity.normalize()

            # Gentle sideways drift when close — avoids pure circular orbiting
            if self.entity.distance_to_target < 200:
                player_pos = self.game.player.pos
                to_player = pygame.math.Vector2(
                    player_pos[0] - entity_pos[0],
                    player_pos[1] - entity_pos[1],
                )
                if to_player.length() > 0:
                    to_player = to_player.normalize()
                    perp = pygame.math.Vector2(-to_player.y, to_player.x)
                    strafe_sign = getattr(self.entity, '_strafe_sign', 1)
                    perp *= strafe_sign
                    desired_velocity = (desired_velocity * 0.75) + (perp * 0.25)
                    if desired_velocity.length() > 0:
                        desired_velocity = desired_velocity.normalize()

            # Slow down near the target tile
            slowing_radius = 24
            speed_modifier = (distance / slowing_radius) if distance < slowing_radius else 1.0
            self.entity.Set_Direction(desired_velocity * speed_modifier)
        else:
            self.entity.Set_Direction(pygame.math.Vector2(0, 0))

    def Set_Movement_Strategy(self, strategy):
        if self.movement_strategy == strategy:
            return
        self.movement_strategy = strategy

    def Get_Distance(self, pos_a, pos_b):
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    # ------------------------------------------------------------------ #
    #  Line-of-sight                                                       #
    # ------------------------------------------------------------------ #
    def Handle_Line_Of_Sight(self, delta_time):
        if self.line_of_sight_cooldown > 0:
            self.line_of_sight_cooldown -= delta_time
        else:
            self.line_of_sight_cooldown = 1.0
            if self.Line_Of_Sight(self.game.player.pos):
                self.player_found = PLAYER_FOUND_MAX
                self.Trigger_Player_Found()

        if self.player_found > 0:
            self.player_found -= delta_time
            return True
        return False

    def Trigger_Player_Found(self):
        if self.entity.alert_cooldown:
            return False
        self.entity.Set_Alert_Cooldown(20)
        self.game.clatter.Generate_Clatter(self.entity.pos, 800)
        return False

    def Line_Of_Sight_Cooldown(self, delta_time):
        if self.line_of_sight_cooldown > 0:
            self.line_of_sight_cooldown -= delta_time
            return False
        self.line_of_sight_cooldown = 1
        return True

    def Line_Of_Sight(self, target_pos):
        tile_size = self.game.tilemap.tile_size
        entity_pos = self.entity.pos

        x1, y1 = entity_pos[0] // tile_size, entity_pos[1] // tile_size
        x2, y2 = target_pos[0] // tile_size, target_pos[1] // tile_size

        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx, sy = (1 if x1 < x2 else -1), (1 if y1 < y2 else -1)
        err = dx - dy

        while (x1, y1) != (x2, y2):
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

            if (x1, y1) == (x2, y2):
                return True
            if not self.game.ray_caster.Check_Tile((x1, y1)):
                return False

        return True