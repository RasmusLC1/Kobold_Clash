from scripts.entities.items.weapons.projectiles.bombs.bomb import Bomb
import math
from scripts.engine.keys.keys import keys


class Bomb_Launcher():
    def __init__(self, game):
        self.game = game
        self.index = 0
        self.bomb_pool = []

            
    def Shoot_Bomb(self, entity, special_attack, bomb_type, target, num_lines=1):
        # Basic raycasting attributes
        spread_angle = 50  # Total spread of the fan (in degrees)
        angle_increment = 0 if num_lines == 1 else spread_angle / (num_lines - 1)

        # Calculate the base angle using atan2(y, x)
        dx = target[0] - entity.pos[0]
        dy = target[1] - entity.pos[1]
        
        base_angle = math.atan2(dy, dx)
        start_angle = base_angle - math.radians(spread_angle / 2)

        speed = 1  # Adjust as needed

        # Generate fire bombs
        for j in range(num_lines):
            bomb = self.Find_Bomb()
            if not bomb:
                bomb = self.Create_Extra_Bomb()
            
            angle = base_angle if num_lines == 1 else start_angle + j * math.radians(angle_increment)
            
            direction = (math.cos(angle) * speed, math.sin(angle) * speed)
            bomb.Set_Enabled(entity.pos, speed, special_attack, direction, target, entity, bomb_type, 120)

    
    # Append extra fire bomb to the pool in case it runs out
    def Create_Extra_Bomb(self):
        bomb = Bomb(
                self.game,
                (-999, -999),
                100
            )
        self.bomb_pool.append(bomb)
        return bomb


    # Search for bombs with an index
    def Find_Bomb(self):
        # If there are no bombs in the pool return None to spawn bomb
        if not self.bomb_pool:
            return None
        
        # Check if the initial index is available, in which case loop the index back to 0
        if not self.bomb_pool[0].delete_countdown:
            self.index = 0
        
        # Overflow prevent
        if self.index >= len(self.bomb_pool) - 1:
            return None

        # Set the fire bomb to be the next available index
        bomb = self.bomb_pool[self.index]
        self.index += 1

        # If there are no free fire bomb return None to spawn a new one
        if bomb.delete_countdown:
            return None
        
        return bomb
