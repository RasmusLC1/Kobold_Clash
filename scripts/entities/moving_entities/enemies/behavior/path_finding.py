
import math
import pygame
import random


class Path_Finding():
    def __init__(self, game, entity) -> None:
        self.game = game
        self.entity = entity

        self.pos_holder = (0,0)
        self.path = [] # Path to destination

        # self.pos in self.game.tilemap.tile_size/self.game.tilemap.tile_size tileformat
        self.src_x = 0
        self.src_y = 0

        # destination in self.game.tilemap.tile_size/self.game.tilemap.tile_size tileformat
        self.des_x = 0
        self.des_y = 0

        self.pos_holder_timer = 0

        self.player_found = False

        self.direct_pathing_cooldown = 0



    def Path_Finding(self, delta_time):
        self.Set_Position_Holder(delta_time)

        self.Corner_Handling()

        # Pathfind towards the target
        if self.entity.Attack_Strategy(delta_time):
            self.entity.Trap_Collision_Handler()

            return
        else:
            # If enemy looses sight of player he will try to go to the last known location
            if self.player_found:
                self.player_found = False
                self.entity.Set_Target(self.game.player.pos)

        if not self.Navigate_Path():
            self.Moving_Random(delta_time)

    # Path to a random part of the dungeon
    # Path towards the position of a random enemy
    # since they all need to be able to reach each other
    # Makes the pathing easier
    def Find_Patrol_Path(self):
        try:
            self.game.enemy_handler.Add_To_Patrol_Queue(self.entity)
        except Exception as e:
            print(f'ERROR FINDING PATROL PATH{e}', self.entity.pos)


    def Navigate_Path(self):
        # Pathfinding
        if len(self.path) < 2:
            return False
        
        # Calculate the updated position
        self.Calculate_Position()
        # Assign the target to be the next position
        target = self.path[1]

        # Move the entity away from walls
        if self.Path_Segment_Complete(target):
            return
        self.Calculate_Path_Segment(target)

        
        return True


    def Calculate_Path_Segment(self, target):
        target_pos = (target[0] * self.game.tilemap.tile_size, target[1] * self.game.tilemap.tile_size)
        self.entity.direction = pygame.math.Vector2(target_pos[0] - self.entity.pos[0], target_pos[1] - self.entity.pos[1])
        if self.entity.direction.length() > 0:
            self.entity.direction.normalize_ip()

    # Check if enemy has reached target, pop the first element and set direction to 0
    def Path_Segment_Complete(self, target):

        # Use a threshold for reaching the target to avoid precision issues
        reach_threshold = self.game.tilemap.tile_size
        if math.hypot(self.entity.pos[0] - target[0] * self.game.tilemap.tile_size, self.entity.pos[1] - target[1] * self.game.tilemap.tile_size) > reach_threshold:
            return False

        self.entity.direction = (0, 0)
        self.path.pop(0)
        return True

    def Find_Shortest_Path(self) -> None:
        # Check if the entity has recently received a new target
   
        self.path.clear()
        self.Calculate_Position()
        self.Calculate_Destination_Position(self.entity.target)
        self.path = self.game.a_star.a_star_search([self.src_x, self.src_y], [self.des_x, self.des_y], self.entity.path_finding_strategy)
        if not self.path:
            return False
        self.path = [(x + self.game.a_star.min_x, y + self.game.a_star.min_y) for (x, y) in self.path]

        
        return True
    

    # Move the entity if they're to close to a wall
    def Corner_Handling(self):        
        direction_x = 0
        direction_y = 0
        if self.entity.collisions['up']:
            direction_y = -2
        if self.entity.collisions['down']:
            direction_y = 2
        if self.entity.collisions['left']:
            direction_x = 2
        if self.entity.collisions['right']:
            direction_x = -2
        if direction_x or direction_y:
            self.entity.Set_Frame_movement((direction_x, direction_y))
            self.entity.Tile_Map_Collision_Detection(self.game.tilemap)




    # Save the entity's position every 200 ticks
    def Set_Position_Holder(self, delta_time):
        if self.pos_holder_timer:
            self.pos_holder_timer -= delta_time
        else:
            self.pos_holder = self.entity.pos.copy()
            self.pos_holder_timer = 3

    
    def Moving_Random(self, delta_time):
        self.entity.Reduce_Movement(4)
        self.entity.direction = (self.entity.direction_x, self.entity.direction_y)
        if self.entity.random_movement_cooldown:
            self.entity.random_movement_cooldown -= delta_time
            return
        self.entity.direction_x = random.randint(-1, 1) 
        self.entity.direction_y = random.randint(-1, 1) 
        
        self.entity.direction = (self.entity.direction_x, self.entity.direction_y)
        self.entity.random_movement_cooldown = 2

        self.entity.Trap_Collision_Handler()

    
    def Calculate_Position(self):
        self.src_x = round(self.entity.pos[0] // self.game.tilemap.tile_size) - self.game.a_star.min_x 
        self.src_y = round(self.entity.pos[1] // self.game.tilemap.tile_size) - self.game.a_star.min_y 
        
    def Calculate_Destination_Position(self, destination):
        self.des_x = round(destination[0] // self.game.tilemap.tile_size) - self.game.a_star.min_x 
        self.des_y = round(destination[1] // self.game.tilemap.tile_size) - self.game.a_star.min_y 

