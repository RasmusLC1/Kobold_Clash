import pygame
import random
from scripts.engine.keys.keys import keys


class Attack_Stategies():

    def __init__(self, game, entity) -> None:
        self.game = game
        self.entity = entity


        self.player_found = 0
        self.player_found_max = 400

        self.direct_pathing_cooldown = 0

    # Return True if pathing updated else false
    def Attack_Strategy(self) -> bool:
        if self.game.player.effects.invisibility.effect:
            return False

        if self.entity.distance_to_player > 300:
            return
        
        self.Update_Player_Found()
        attack_strategy = self.entity.attack_strategy 
        if attack_strategy == keys.direct: # charge the player
            return self.Direct_Pathing()
        elif attack_strategy == keys.long_range: # keep long distance
            return self.Keep_Distance(200, 160)
        elif attack_strategy == keys.medium_range: # keep medium distance
            return self.Keep_Distance(120, 80)
        elif attack_strategy == keys.short_range:
            return self.Keep_Distance(80, 40)
        elif attack_strategy == keys.keep_position:
            self.entity.direction = (0, 0)
        elif attack_strategy == keys.idle:
            return False
        elif attack_strategy == keys.run_away:
            return False
        else:
            return self.Direct_Pathing()
        

    def Update_Player_Found(self):
        if not self.player_found:
            return False
        self.player_found -= 1
        return True

    def Keep_Distance(self, max_range, closest_range):
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

    # Enemies check for line of sight and sets player found cooldown accordingly
    def Handle_Line_Of_Sight(self):
        if not self.Line_Of_Sight(self.game.player.pos):
            if not self.player_found:
                return False
        else:
            self.player_found = self.player_found_max
            return True

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
            # Only update every 1000 ticks since you don't want
            # the enemies to spam the ability and lag the game
            if not self.entity.alert_cooldown:
                self.entity.Set_Alert_Cooldown(20)
                self.game.clatter.Generate_Clatter(self.entity.pos, 400) # Generate clatter to alert nearby enemies
            self.direct_pathing_cooldown = 10
            return True
        return False
    

    # Check for line of sight with target, returns true when found
    def Line_Of_Sight(self, target_pos):
        tile_size = self.game.tilemap.tile_size

        # Convert enemy’s pixel position to tile coordinates
        ex = int(self.entity.pos[0] // tile_size)
        ey = int(self.entity.pos[1] // tile_size)
        # Convert player’s pixel position to tile coordinates
        px = int(target_pos[0] // tile_size)
        py = int(target_pos[1] // tile_size)

        # Generate the list of tiles along the line
        line_tiles = self.bresenham_line((ex, ey), (px, py))

        # Check each tile. If any tile is not see-through, return False
        for (tx, ty) in line_tiles:
            tile_key = f"{tx};{ty}"
            # If your ray_caster.Check_Tile(tile_key) means "can see through" is True
            # or "walkable" is True, adapt accordingly.
            if not self.game.ray_caster.Check_Tile(tile_key):
                return False

        return True

    # Returns all the tile coordinates on a line between `start` and `end`.
    # start/end should be (x, y) tuples in tile coordinates (integer grid positions).    
    def bresenham_line(self, start, end):

        x1, y1 = start
        x2, y2 = end

        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break

            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return points
