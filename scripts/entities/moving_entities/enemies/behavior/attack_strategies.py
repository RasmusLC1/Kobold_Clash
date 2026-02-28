import pygame
import random
import math

from scripts.engine.keys.keys import keys


class Attack_Stategies():

    def __init__(self, game, entity) -> None:
        self.game = game
        self.entity = entity


        self.player_found = 0
        self.player_found_max = 10 # 10 seconds

        self.line_of_sight_cooldown = 0

        self.direct_pathing_cooldown = 0

        self.target_tile_pos = None

        self.in_range_cooldown = 0

        self.tile_check_timestamp = 0
        # None if no range needed
        self.attack_ranges = {
            keys.long_range: (200, 160),
            keys.medium_range: (120, 80),
            keys.short_range: (80, 60),
            keys.direct: (0, 20),
            keys.keep_position: None,
            keys.idle: None,
            keys.run_away: None
        }


        

    # Return True if pathing updated else false
    def Attack_Strategy(self, delta_time) -> bool:
        if self.game.player.effects.invisibility.effect:
            return False

        if self.entity.distance_to_player > 300:
            return False
        
        # Check if the enemy has line of sight if not return
        # TODO: Go to players last known tile
        if not self.Handle_Line_Of_Sight(delta_time):
            return False
        
        attack_strategy = self.entity.attack_strategy 

        attack_range = self.attack_ranges.get(attack_strategy)

        if not attack_range:
            return False
        
        # Only update movement when the entity needs to move
        # If entity in range, check less often
        if self.in_range_cooldown <= 0:
            self.Update_Movement_Logic(delta_time)
        else:
            self.in_range_cooldown -= delta_time

        return True



    
    def Update_Movement_Logic(self, delta_time):
              
        # Returns false if destination needs to be updated
        if not self.Move_Enemy_Towards_Destination(): 
            return False
            

        
        
    
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
        tiles_in_range = self.Find_Tiles_In_Range(entity_player_distance, max_range,
                           min_range)
        
        if not tiles_in_range:
            return None
        # Safety check: if no tiles found, exit
        num_tiles = len(tiles_in_range)
        if num_tiles == 0:
            return None

        tiles_in_range.sort(key=lambda x: x[0])

        target_tile =  self.Choose_Destination(entity_player_distance, max_range,
                           min_range, num_tiles, tiles_in_range)
        
        if not target_tile:
            return None
        
        self.target_tile_pos = target_tile.scaled_pos
        
        return self.target_tile_pos

    def Find_Tiles_In_Range(self, entity_player_distance, max_range,
                           min_range):
        # Get surrounding tiles
        surrounding_tiles = self.game.tilemap.Get_Floor_Tiles_Around(self.entity.pos)
        # If in range, 90% chance to stay put (return None)
        if min_range < entity_player_distance < max_range:
            if random.randint(1, 10) <= 9: # 90% chance to stand still
                return None

        tiles_in_range = []
        for tile in surrounding_tiles:
            distance = tile.Get_Distance_To_Player()
            if distance is None:
                continue
            # Store the TILE object, not just tile.pos
            tiles_in_range.append((distance, tile))

        
        return tiles_in_range

    # Returns the target position
    def Choose_Destination(self, entity_player_distance, max_range,
                           min_range, num_tiles, tile_data):
        if entity_player_distance > max_range:
            # TOO FAR: Pick from the closest tiles (start of sorted list)
            limit = min(3, num_tiles)
            chosen_tile = tile_data[random.randint(0, limit - 1)]
            return chosen_tile[1]
            
        elif entity_player_distance < min_range:
            # TOO CLOSE: Pick from the furthest tiles (end of sorted list)
            limit_idx = max(0, num_tiles - 3)
            chosen_tile = tile_data[random.randint(limit_idx, num_tiles - 1)]
            return chosen_tile[1]
            
        else:
            # IN RANGE 10 % chance to move
            mid = num_tiles // 2
            idx = random.randint(max(0, mid-1), min(num_tiles-1, mid+1))
            self.in_range_cooldown = 1 # 1 second cooldown, prevents extra calculations and jitters
            return tile_data[idx][1]
        
    def Move_Enemy_Towards_Destination(self):
        
        entity_pos = self.entity.pos
        
        # If no target tile exists find one
        if not self.target_tile_pos:
            if not self.Find_Tile_To_Pathfind_To():
                return False
            

        # If the entity is close to the target, find new tile
        distance_to_tile = self.Get_Distance(entity_pos, self.target_tile_pos)

        if distance_to_tile < 20:
            if not self.Find_Tile_To_Pathfind_To(): # Try to find new tile
                return False
            
        self.Calculate_Direction(entity_pos)
        
        return True

    def Calculate_Direction(self, entity_pos):
        dx = self.target_tile_pos[0] - entity_pos[0] 
        dy = self.target_tile_pos[1] - entity_pos[1] 
            
        new_entity_direction = pygame.math.Vector2(dx, dy)
        self.entity.Set_Direction(new_entity_direction, "MOVE TOWARDS ENEMY POS")

    def Get_Distance(self, pos_a, pos_b):
        """Calculates Euclidean distance between two (x, y) tuples."""
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        return math.sqrt(dx**2 + dy**2)

# LINE OF SIGHT LOGIC
    # Enemies check for line of sight and sets player found cooldown accordingly
    def Handle_Line_Of_Sight(self, delta_time):
        # Return true if the enemy can already see the player
        if not self.Line_Of_Sight_Cooldown(delta_time): 
            return True

        if not self.Line_Of_Sight(self.game.player.pos): # Line of sight blocked
            return False
        else:
            self.Trigger_Player_Found()
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
    

    
