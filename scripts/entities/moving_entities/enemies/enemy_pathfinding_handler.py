import random
from collections import deque
import math

class Enemy_Pathfinding_Handler():
    def __init__(self, game):
        self.game = game
        # deques give O(1) performance for popping from the front of the queue
        self.pathfinding_queue = deque()
        self.pathfinding_queue_cooldown = 0.0

        self.patrol_queue = deque()
        self.patrol_queue_cooldown = 0.0

    def Update(self, delta_time):
        self.Update_Pathfinding_Queue(delta_time)
        self.Update_Patrol_Queue(delta_time)

    def Add_To_Pathfinding_Queue(self, enemy, destination):
        if enemy in self.pathfinding_queue:
            return
        
        if enemy in self.patrol_queue:
            self.patrol_queue.remove(enemy)

        self.pathfinding_queue.append(enemy)
        enemy.Set_Target(destination)

    def Update_Pathfinding_Queue(self, delta_time):
        if not self.pathfinding_queue:
            return
        
        if self.pathfinding_queue_cooldown > 0:
            self.pathfinding_queue_cooldown = max(0.0, self.pathfinding_queue_cooldown - delta_time)
            return
        
        # Safe Object Validation: Drop dead or deleted enemies instantly
        enemy = self.pathfinding_queue.popleft()
        if enemy in self.game.enemy_handler.enemies and enemy.health > 0:
            enemy.Find_New_Path()
            # Cooldown represented in seconds (e.g., 0.5 seconds between combat pathfinds)
            self.pathfinding_queue_cooldown = 0.5 

    def Sort_Pathfinding_Queue(self):
        # Sort back into a list based on distance to simulate sound travel speed, then wrap in deque
        player_pos = self.game.player.pos
        sorted_list = sorted(
            self.pathfinding_queue,
            key=lambda entity: math.hypot(entity.pos[0] - player_pos[0], entity.pos[1] - player_pos[1])
        )
        self.pathfinding_queue = deque(sorted_list)

    def Add_To_Patrol_Queue(self, enemy):
        enemy_target = self.Get_Random_Enemy()
        if not enemy_target:
            return
        
        destination = enemy_target.pos

        if enemy in self.patrol_queue or enemy in self.pathfinding_queue:
            return
            
        self.patrol_queue.append(enemy)
        enemy.Set_Target(destination)
        enemy.Set_On_Patrol(True)

    def Update_Patrol_Queue(self, delta_time):
        if not self.patrol_queue:
            return
        
        if self.patrol_queue_cooldown > 0:
            self.patrol_queue_cooldown = max(0.0, self.patrol_queue_cooldown - delta_time)
            return
        
        enemy = self.patrol_queue.popleft()
        if enemy in self.game.enemy_handler.enemies and enemy.health > 0:
            enemy.Find_New_Path()
            # Patrol requests can happen less frequently (e.g., 1.5 seconds)
            self.patrol_queue_cooldown = 1.5


    def Find_Enemy(self, ID):
        for enemy in self.game.enemy_handler.enemies:
            if enemy.ID == ID:
                return enemy
        return None
    
    def Get_Random_Enemy(self):
        if not self.game.enemy_handler.enemies:
            return None
        return random.choice(self.game.enemy_handler.enemies)