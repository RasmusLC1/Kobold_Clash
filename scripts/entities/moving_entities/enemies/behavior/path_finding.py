
import math
import pygame

# Responsible for navigating dungeon
class Path_Finding():
    def __init__(self, game, entity, path_finding_strategy) -> None:
        self.game = game
        self.entity = entity
        self.path_finding_strategy = path_finding_strategy # Maptype that is used for navigation

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


    def Save_Data(self):
        self.entity.saved_data['path'] = self.path
        self.entity.saved_data['src_x'] = self.src_x
        self.entity.saved_data['src_y'] = self.src_y
        self.entity.saved_data['des_x'] = self.des_x
        self.entity.saved_data['des_y'] = self.des_y
        self.entity.saved_data['player_found'] = self.player_found


    def Load_Data(self, data):
        self.path = data['path']
        self.src_x = data['src_x']
        self.src_y = data['src_y']
        self.des_x = data['des_x']
        self.des_y = data['des_y']
        self.player_found = data['player_found']

    def Path_Finding(self, delta_time):
        # Pathfind towards the target
        if self.entity.Movement_Strategy(delta_time):
            return
        else:
            # If enemy looses sight of player he will try to go to the last known location
            if self.player_found:
                self.player_found = False
                self.entity.Set_Target()

        self.Navigate_Path()

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
        direction = pygame.math.Vector2(target_pos[0] - self.entity.pos[0], target_pos[1] - self.entity.pos[1])
        self.entity.Set_Direction(direction) 

    # Check if enemy has reached target, pop the first element and set direction to 0
    def Path_Segment_Complete(self, target):

        # Use a threshold for reaching the target to avoid precision issues
        reach_threshold = self.game.tilemap.tile_size
        if math.hypot(self.entity.pos[0] - target[0] * self.game.tilemap.tile_size, self.entity.pos[1] - target[1] * self.game.tilemap.tile_size) > reach_threshold:
            return False
        direction = pygame.math.Vector2(0, 0)
        self.entity.Set_Direction(direction) 
        self.path.pop(0)
        return True

    def Find_Shortest_Path(self) -> None:
        # Check if the entity has recently received a new target
   
        self.path.clear()
        self.Calculate_Position()
        self.Calculate_Destination_Position(self.entity.target)
        self.path = self.game.a_star.a_star_search([self.src_x, self.src_y], [self.des_x, self.des_y], self.path_finding_strategy)
        if not self.path:
            return False
        self.path = [(x + self.game.a_star.min_x, y + self.game.a_star.min_y) for (x, y) in self.path]

        
        return True

    
    def Calculate_Position(self):
        self.src_x = round(self.entity.pos[0] // self.game.tilemap.tile_size) - self.game.a_star.min_x 
        self.src_y = round(self.entity.pos[1] // self.game.tilemap.tile_size) - self.game.a_star.min_y 
        
    def Calculate_Destination_Position(self, destination):
        self.des_x = round(destination[0] // self.game.tilemap.tile_size) - self.game.a_star.min_x 
        self.des_y = round(destination[1] // self.game.tilemap.tile_size) - self.game.a_star.min_y 
