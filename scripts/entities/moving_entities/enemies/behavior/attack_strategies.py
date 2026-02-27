import pygame
import random
from scripts.engine.keys.keys import keys


class Attack_Stategies():

    def __init__(self, game, entity) -> None:
        self.game = game
        self.entity = entity


        self.player_found = 0
        self.player_found_max = 10 # 10 seconds

        self.line_of_sight_cooldown = 0

        self.direct_pathing_cooldown = 0

        self.tile_check_timestamp = 0
        # None if no range needed
        self.attack_ranges = {
            keys.long_range: (200, 160),
            keys.medium_range: (120, 80),
            keys.short_range: (80, 60),
            keys.keep_position: None,
            keys.idle: None,
            keys.run_away: None
        }


        

    # Return True if pathing updated else false
    def Attack_Strategy(self, delta_time) -> bool:
        if self.game.player.effects.invisibility.effect:
            return False

        if self.entity.distance_to_player > 300:
            return
        
        # Check if the enemy has line of sight
        if not self.Handle_Line_Of_Sight(delta_time):
            return False
        
        attack_strategy = self.entity.attack_strategy 

        if attack_strategy == keys.direct: # charge the player
            return self.Direct_Pathing()
        
        attack_range = self.attack_ranges.get(attack_strategy)

        if not attack_range:
            return False

        return self.Keep_Distance(attack_range, delta_time)

        

    
    def Keep_Distance(self, ranges, delta_time):
        max_range, closest_range = ranges
        # Cooldown since the player's relative position does not need constant update
        if self.Pathfinding_Cooldown(delta_time):
            return True
        
        if self.entity.distance_to_player < max_range and self.entity.distance_to_player > closest_range:
            
            path = self.Find_Escape_Path()

            self.direct_pathing_cooldown = 40
            if not path:
                return True
            
            self.entity.direction = pygame.math.Vector2(path[0], path[1])
            self.entity.direction.normalize_ip()

            return True
        
        if self.entity.distance_to_player > max_range :
            return self.Charge_player(150)
        
        return self.Run_Away(60)
    
    def Pathfinding_Cooldown(self, delta_time):
        if self.direct_pathing_cooldown > 0:
            self.direct_pathing_cooldown -= delta_time
            return True
        return False

# NEW METHOD
    def Find_Tile_To_Pathfind_To(self):
        attack_strategy = self.entity.attack_strategy 
        max_range, min_range = self.attack_ranges.get(attack_strategy, (0, 0))
        
        if max_range == 0:
            return None
            
        entity_player_distance = self.entity.distance_to_player
        tile_data = self.Find_Tiles_In_Range(entity_player_distance, max_range,
                           min_range, tile_data)
        # Safety check: if no tiles found, exit
        num_tiles = len(tile_data)
        if num_tiles == 0:
            return None

        tile_data.sort(key=lambda x: x[0])

        return self.Choose_Destination(entity_player_distance, max_range,
                           min_range, num_tiles, tile_data)

    def Find_Tiles_In_Range(self, entity_player_distance, max_range,
                           min_range, tile_data):
        # Get surrounding tiles
        surrounding_tiles = self.game.tilemap.Get_Floor_Tiles_Around(self.entity.pos)
        # If in range, 90% chance to stay put (return None)
        if min_range < entity_player_distance < max_range:
            if random.randint(1, 10) <= 9: # 90% chance to stand still
                return None

        tile_data = []
        for tile in surrounding_tiles:
            distance = tile.Get_Distance_To_Player()
            if distance is None:
                continue
            # Store the TILE object, not just tile.pos
            tile_data.append((distance, tile))

        
        return tile_data

    # Returns the target position
    def Choose_Destination(self, entity_player_distance, max_range,
                           min_range, num_tiles, tile_data):
        if entity_player_distance > max_range:
            # TOO FAR: Pick from the closest tiles (start of sorted list)
            limit = min(3, num_tiles)
            chosen_pair = tile_data[random.randint(0, limit - 1)]
            return chosen_pair[1]
            
        elif entity_player_distance < min_range:
            # TOO CLOSE: Pick from the furthest tiles (end of sorted list)
            limit_idx = max(0, num_tiles - 3)
            chosen_pair = tile_data[random.randint(limit_idx, num_tiles - 1)]
            return chosen_pair[1]
            
        else:
            # IN RANGE (The 10% chance): Shuffle around slightly
            mid = num_tiles // 2
            idx = random.randint(max(0, mid-1), min(num_tiles-1, mid+1))
            return tile_data[idx][1]
        
    def Move_Enemy_Towards_Destination(self, target_pos):
        dx = target_pos[0] - self.entity.pos[0]
        dy = target_pos[1] - self.entity.pos[1]
        self.entity.direction = pygame.math.Vector2(dx, dy)
        if self.entity.direction[0] == 0 and self.entity.direction[1] == 0:
            return False
        self.entity.direction.normalize_ip()
        
        return True

# LINE OF SIGHT LOGIC
    # Enemies check for line of sight and sets player found cooldown accordingly
    def Handle_Line_Of_Sight(self, delta_time):
        if not self.Line_Of_Sight_Cooldown(delta_time):
            return False

        if not self.Line_Of_Sight(self.game.player.pos): # Line of sight blocked
            return False
        else:
            self.Trigger_Player_Found(delta_time)
            return True
        
    # Alert other nearby enemies
    def Trigger_Player_Found(self):
        # Check if entity has recently been triggered
        if self.entity.alert_cooldown:
            return False
 
        self.entity.Set_Alert_Cooldown(20)
        self.game.clatter.Generate_Clatter(self.entity.pos, 800) # Generate clatter to alert nearby enemies
        return False

    def Line_Of_Sight_Cooldown(self, delta_time):
        if self.line_of_sight_cooldown > 0:
            self.line_of_sight_cooldown -= delta_time
            return False
        
        self.line_of_sight_cooldown = 1 # Check line of sight 1 time per second
        return True

    
    # Returns true if line of sight to target, else false
    def Line_Of_Sight(self, target_pos):
        tile_size = self.game.tilemap.tile_size
        
        # Current tile (Start)
        x1, y1 = int(self.entity.pos[0] // tile_size), int(self.entity.pos[1] // tile_size)
        # Target tile (End)
        x2, y2 = int(target_pos[0] // tile_size), int(target_pos[1] // tile_size)

        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx, sy = (1 if x1 < x2 else -1), (1 if y1 < y2 else -1)
        err = dx - dy

        # Loop until we reach the target tile
        while (x1, y1) != (x2, y2):
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
                
            # If we reach the target tile, we have a clear line of sight
            if (x1, y1) == (x2, y2):
                return True

            # Check if the current tile is solid
            if not self.game.ray_caster.Check_Tile((x1, y1)):
                return False

        return True
    

# OLD LOGIC
    def Keep_Distance(self, ranges):
        max_range, closest_range = ranges
        # Cooldown since the player's relative position does not need constant update
        if self.direct_pathing_cooldown:
            self.direct_pathing_cooldown = max(0, self.direct_pathing_cooldown - 1)
            return True       
        
        if self.entity.distance_to_player < max_range and self.entity.distance_to_player > closest_range:
            
            path = self.Find_Escape_Path()

            self.direct_pathing_cooldown = 40
            if not path:
                return True
            
            self.entity.direction = pygame.math.Vector2(path[0], path[1])
            self.entity.direction.normalize_ip()

            return True
        
        if self.entity.distance_to_player > max_range :
            return self.Charge_player(150)
        
        return self.Run_Away(60)

    # Find an escape path and ensure that there are no walls in the way
    def Find_Escape_Path(self):
        iterations = 0

        speed_modifier = self.game.tilemap.tile_size * self.entity.agility * 2
        while True:
            random_x = (random.randint(1, 10) / 10) * random.choice([-1, 1])
            random_y = (random.randint(1, 10) / 10) * random.choice([-1, 1])

            # Check for tiles along the escape path
            target_pos = (self.entity.pos[0] + random_x * speed_modifier, self.entity.pos[1] + random_y * speed_modifier)
            if self.Line_Of_Sight(target_pos):
                return (random_x, random_y)
            iterations += 1
            if iterations > 10:
                break
            
        return None

    def Direct_Pathing(self):
        # Cooldown since the player's relative position does not need constant update
        if self.direct_pathing_cooldown:
            self.direct_pathing_cooldown = max(0, self.direct_pathing_cooldown - 1)
            return True
        return self.Charge_player(200)  
        # Player is close, so the enemy charge directly
        
    def Run_Away(self, distance):
        if self.entity.distance_to_player < distance or self.player_found:
            # Check if the enemy has 
            if not self.Handle_Line_Of_Sight():
                return False

            dx = (self.game.player.pos[0] - self.entity.pos[0]) * -1
            dy = (self.game.player.pos[1] - self.entity.pos[1]) * -1
            self.entity.direction = pygame.math.Vector2(dx, dy)
            if self.entity.direction[0] == 0 and self.entity.direction[1] == 0:
                return False
            
            self.entity.direction.normalize_ip()
            if not self.entity.alert_cooldown:
                self.entity.Set_Alert_Cooldown(7)
                self.game.clatter.Generate_Clatter(self.entity.pos, 400) # Generate clatter to alert nearby enemies
            self.direct_pathing_cooldown = 10
            return True
        
        return False

    
    def Charge_player(self, distance):
        if self.entity.distance_to_player < distance or self.player_found:
            # Check if the enemy has 
            if not self.Handle_Line_Of_Sight():
                return False
            dx = self.game.player.pos[0] - self.entity.pos[0]
            dy = self.game.player.pos[1] - self.entity.pos[1]
            self.entity.direction = pygame.math.Vector2(dx, dy)
            if self.entity.direction[0] == 0 and self.entity.direction[1] == 0:
                return False
            self.entity.direction.normalize_ip()
            # Only update every 20 seconds since you don't want
            # the enemies to spam the ability and lag the game
            if not self.entity.alert_cooldown:
                self.entity.Set_Alert_Cooldown(20)
                self.game.clatter.Generate_Clatter(self.entity.pos, 400) # Generate clatter to alert nearby enemies
            self.direct_pathing_cooldown = 10
            return True
        return False
    

    
